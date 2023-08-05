# Copyright 2017 - Nokia Networks
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

from cachetools import cached
from cachetools import LRUCache
import json
import jwt
import memcache
from oslo_config import cfg
from oslo_log import log as logging
from oslo_middleware import base as base_middleware
import pprint
import requests
from six.moves import urllib
import webob.dec

from glare.common import exception
from glare.common import utils
from glare.i18n import _
from jwt.algorithms import RSAAlgorithm

LOG = logging.getLogger(__name__)

keycloak_oidc_opts = [
    cfg.StrOpt(
        'auth_url',
        default='http://127.0.0.1:8080/auth',
        help='Keycloak base url (e.g. https://my.keycloak:8443/auth)'
    ),
    cfg.StrOpt(
        'user_info_endpoint_url',
        default='/realms/%s/protocol/openid-connect/userinfo',
        help='Endpoint against which authorization will be performed'
    ),
    cfg.StrOpt(
        'certfile',
        help='Required if identity server requires client certificate'
    ),
    cfg.StrOpt(
        'keyfile',
        help='Required if identity server requires client certificate'
    ),
    cfg.StrOpt(
        'cafile',
        help='A PEM encoded Certificate Authority to use when verifying '
             'HTTPs connections. Defaults to system CAs.'
    ),
    cfg.BoolOpt(
        'insecure',
        default=False,
        help='If True, SSL/TLS certificate verification is disabled'
    ),
    cfg.StrOpt(
        'memcached_server',
        default=None,
        help='Url of memcached server to use for caching'
    ),
    cfg.IntOpt(
        'token_cache_time',
        default=60,
        min=0,
        help='In order to prevent excessive effort spent validating '
             'tokens, the middleware caches previously-seen tokens '
             'for a configurable duration (in seconds).'
    ),
    cfg.StrOpt(
        'public_cert_url',
        default="/realms/%s/protocol/openid-connect/certs",
        help="URL to get the public key for perticualar realm"
    ),
    cfg.StrOpt(
        'keycloak_iss',
        help="keycloak issuer(iss) url Ex: https://ip_add:port/auth/realms/%s"
    )
]

CONF = cfg.CONF
CONF.register_opts(keycloak_oidc_opts, group="keycloak_oidc")


class KeycloakAuthMiddleware(base_middleware.Middleware):
    def __init__(self, app):
        super(KeycloakAuthMiddleware, self).__init__(application=app)
        mcserv_url = CONF.keycloak_oidc.memcached_server
        self.mcclient = memcache.Client(mcserv_url) if mcserv_url else None
        self.certfile = CONF.keycloak_oidc.certfile
        self.keyfile = CONF.keycloak_oidc.keyfile
        self.cafile = CONF.keycloak_oidc.cafile or utils.get_system_ca_file()
        self.insecure = CONF.keycloak_oidc.insecure

    def authenticate(self, access_token, realm_name, audience):
        info = None
        if self.mcclient:
            info = self.mcclient.get(access_token)

        user_info_endpoint_url = CONF.keycloak_oidc.user_info_endpoint_url
        if info is None:
            if user_info_endpoint_url.startswith(('http://', 'https://')):
                info = self.send_request_to_auth_server(
                    url=user_info_endpoint_url, access_token=access_token)
            else:
                public_key = self.get_public_key(realm_name)
                keycloak_iss = None
                try:
                    if CONF.keycloak_oidc.keycloak_iss:
                        keycloak_iss = \
                            CONF.keycloak_oidc.keycloak_iss % realm_name
                    jwt.decode(access_token, public_key, audience=audience,
                               issuer=keycloak_iss, algorithms=['RS256'],
                               verify=True)
                except Exception as e:
                    LOG.error("Exception in access_token validation %s", e)
                    raise exception.Unauthorized()
        return info

    @webob.dec.wsgify
    def __call__(self, request):
        if 'X-Auth-Token' not in request.headers:
            msg = _("Auth token must be provided in 'X-Auth-Token' header.")
            LOG.error(msg)
            raise exception.Unauthorized()
        access_token = request.headers.get('X-Auth-Token')
        try:
            decoded = jwt.decode(access_token, algorithms=['RS256'],
                                 verify=False)
        except Exception as e:
            msg = _("Token can't be decoded because of wrong format %s")\
                % str(e)
            LOG.error(msg)
            raise exception.Unauthorized()

        # Get user realm from parsed token
        # Format is "iss": "http://<host>:<port>/auth/realms/<realm_name>",
        __, __, realm_name = decoded['iss'].strip().rpartition('/realms/')
        audience = decoded.get('aud')

        # Get roles from from parsed token
        roles = ','.join(decoded['realm_access']['roles']) \
            if 'realm_access' in decoded else ''

        self.authenticate(access_token, realm_name, audience)

        request.headers["X-Identity-Status"] = "Confirmed"
        request.headers["X-Project-Id"] = realm_name
        request.headers["X-Roles"] = roles
        return request.get_response(self.application)

    @cached(LRUCache(maxsize=32))
    def get_public_key(self, realm_name):
        keycloak_key_url = CONF.keycloak_oidc.auth_url + \
            CONF.keycloak_oidc.public_cert_url % realm_name
        response_json = self.send_request_to_auth_server(keycloak_key_url)
        public_key = RSAAlgorithm.from_jwk(json.dumps(
            response_json.get("keys")[0]))
        return public_key

    def send_request_to_auth_server(self, url, access_token=None):
        verify = None
        if urllib.parse.urlparse(url).scheme == "https":
            verify = False if self.insecure else self.cafile

        cert = (self.certfile, self.keyfile) \
            if self.certfile and self.keyfile else None

        headers = {}
        if access_token:
            headers["Authorization"] = "Bearer %s" % access_token
        try:
            resp = requests.get(
                url,
                headers=headers,
                verify=verify,
                cert=cert
            )
        except requests.ConnectionError as e:
            msg = _("Can't connect to keycloak server with address '%s'."
                    ) % url
            LOG.error(msg, e)
            raise exception.GlareException(message=msg)

        if resp.status_code == 400:
            raise exception.BadRequest(message=resp.text)
        if resp.status_code == 401:
            LOG.warning("HTTP response from OIDC provider:"
                        " [%s] with WWW-Authenticate: [%s]",
                        pprint.pformat(resp.text),
                        resp.headers.get("WWW-Authenticate"))
            raise exception.Unauthorized(message=resp.text)
        if resp.status_code == 403:
            raise exception.Forbidden(message=resp.text)
        elif resp.status_code > 400:
            raise exception.GlareException(message=resp.text)
        return resp.json()
