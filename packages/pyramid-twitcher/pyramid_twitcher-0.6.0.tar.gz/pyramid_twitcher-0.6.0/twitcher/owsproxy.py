"""
The owsproxy is a service which acts as a proxy for registered OWS services.

The implementation of owsproxy is based on `papyrus_ogcproxy <https://github.com/elemoine/papyrus_ogcproxy>`_

See also: https://github.com/nive/outpost/blob/master/outpost/proxy.py
"""
import requests

from pyramid.response import Response
from pyramid.settings import asbool
from typing import TYPE_CHECKING

from twitcher.owsexceptions import OWSAccessForbidden, OWSAccessFailed
from twitcher.utils import (
    replace_caps_url,
    get_settings,
    get_twitcher_url,
    is_valid_url)

import logging
LOGGER = logging.getLogger('TWITCHER')

if TYPE_CHECKING:
    from twitcher.typedefs import AnySettingsContainer  # noqa: F401
    from pyramid.config import Configurator             # noqa: F401
    from typing import AnyStr                           # noqa: F401


allowed_content_types = (
    "application/xml",                       # XML
    "text/xml",
    "text/xml;charset=ISO-8859-1"
    "application/vnd.ogc.se_xml",            # OGC Service Exception
    "application/vnd.ogc.se+xml",            # OGC Service Exception
    # "application/vnd.ogc.success+xml",      # OGC Success (SLD Put)
    "application/vnd.ogc.wms_xml",           # WMS Capabilities
    # "application/vnd.ogc.gml",              # GML
    # "application/vnd.ogc.sld+xml",          # SLD
    "application/vnd.google-earth.kml+xml",  # KML
    "application/vnd.google-earth.kmz",
    "image/png",                             # PNG
    "image/png;mode=32bit",
    "image/gif",                             # GIF
    "image/jpeg",                            # JPEG
    "application/json",                      # JSON
    "application/json;charset=ISO-8859-1",
)

# TODO: configure allowed hosts
allowed_hosts = (
    # list allowed hosts here (no port limiting)
    # "localhost",
)


# requests.models.Response defaults its chunk size to 128 bytes, which is very slow
class BufferedResponse(object):
    def __init__(self, resp):
        self.resp = resp

    def __iter__(self):
        return self.resp.iter_content(64 * 1024)


def _send_request(request, service, extra_path=None, request_params=None):

    # TODO: fix way to build url
    url = service['url']
    if extra_path:
        url += '/' + extra_path
    if request_params:
        url += '?' + request_params
    LOGGER.debug('url = {}'.format(url))

    # forward request to target (without Host Header)
    h = dict(request.headers)
    h.pop("Host", h)
    h['Accept-Encoding'] = None
    #
    service_type = service.get('type', 'wps')
    service_verify = service.get('verify', True)
    if service_type and (service_type.lower() != 'wps'):
        try:
            resp_iter = requests.request(method=request.method.upper(), url=url, data=request.body, headers=h,
                                         stream=True, verify=service_verify)
        except Exception as e:
            return OWSAccessFailed("Request failed: {}".format(e))

        # Headers meaningful only for a single transport-level connection
        hop_by_hop = ['connection', 'keep-alive', 'public', 'proxy-authenticate', 'transfer-encoding', 'upgrade']
        return Response(app_iter=BufferedResponse(resp_iter),
                        headers={k: v for k, v in list(resp_iter.headers.items()) if k.lower() not in hop_by_hop},
                        status_code=resp_iter.status_code)
    else:
        try:
            resp = requests.request(method=request.method.upper(), url=url, data=request.body, headers=h,
                                    verify=service_verify)
        except Exception as e:
            return OWSAccessFailed("Request failed: {}".format(e))

        if resp.ok is False:
            if 'ExceptionReport' in resp.text:
                pass
            else:
                return OWSAccessFailed("Response is not ok: {}".format(resp.reason))

        # check for allowed content types
        ct = None
        # LOGGER.debug("headers=", resp.headers)
        if "Content-Type" in resp.headers:
            ct = resp.headers["Content-Type"]
            if not ct.split(";")[0] in allowed_content_types:
                msg = "Content type is not allowed: {}.".format(ct)
                LOGGER.error(msg)
                return OWSAccessForbidden(msg)
        else:
            # return OWSAccessFailed("Could not get content type from response.")
            LOGGER.warn("Could not get content type from response")

        try:
            if ct in ['text/xml', 'application/xml', 'text/xml;charset=ISO-8859-1']:
                # replace urls in xml content
                # ... if public URL is not configured use proxy url.
                if is_valid_url(service.get('purl')):
                    public_url = service['purl']
                else:
                    public_url = request.route_url('owsproxy', service_name=service['name'])
                # TODO: where do i need to replace urls?
                content = replace_caps_url(resp.content, public_url, service['url'])
            else:
                # raw content
                content = resp.content
        except Exception:
            return OWSAccessFailed("Could not decode content.")

        headers = {}
        if ct:
            headers["Content-Type"] = ct
        return Response(content, status=resp.status_code, headers=headers)


def owsproxy_base_path(container):
    # type: (AnySettingsContainer) -> AnyStr
    settings = get_settings(container)
    return settings.get('twitcher.ows_proxy_protected_path', '/ows').rstrip('/').strip()


def owsproxy_base_url(container):
    # type: (AnySettingsContainer) -> AnyStr
    twitcher_url = get_twitcher_url(container)
    owsproxy_path = owsproxy_base_path(container)
    return twitcher_url + owsproxy_path


def owsproxy_view(request):
    try:
        service_name = request.matchdict.get('service_name')
        extra_path = request.matchdict.get('extra_path')
        service = request.owsregistry.get_service_by_name(service_name)
    except Exception:
        return OWSAccessFailed("Could not find service")
    if request.is_verified is False:
        raise OWSAccessForbidden("Access to service is forbidden.")
    return _send_request(request, service, extra_path, request_params=request.query_string)


def owsproxy_defaultconfig(config):
    # type: (Configurator) -> None
    settings = get_settings(config)
    if asbool(settings.get('twitcher.ows_proxy', True)):
        protected_path = owsproxy_base_path(settings)

        config.include('twitcher.oauth2')
        config.include('twitcher.owsregistry')
        config.include('twitcher.owssecurity')
        config.add_route('owsproxy', protected_path + '/proxy/{service_name}')
        config.add_route('owsproxy_extra', protected_path + '/proxy/{service_name}/{extra_path:.*}')
        config.add_view(owsproxy_view, route_name='owsproxy')
        config.add_view(owsproxy_view, route_name='owsproxy_extra')


def includeme(config):
    from twitcher.adapter import get_adapter_factory
    get_adapter_factory(config).owsproxy_config(config)
