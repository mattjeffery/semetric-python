#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Copyright (C) 2013  Matt Jeffery <matt@clan.se>
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

import sys
import httplib2
import logging

# Special imports for Python 3
if sys.version_info >= (3,): # pragma: no cover
    from urllib.parse import urlparse, urlunparse, urlencode, parse_qs
    basestring = str
else: # pragma: no cover
    from urllib import urlencode
    from urlparse import urlparse, urlunparse, parse_qs

try:
    import json
except ImportError: # pragma: no cover
    import simplejson as json

from operator import itemgetter

from semetric.apiclient import __project__, __version__
from semetric.apiclient.entity import *
from semetric.apiclient.exc import APIError

log = logging.getLogger(__name__)

class APIClient(object):
    """
        API Client
    """

    API_BASE_URL = "http://api.semetric.com"
    HTTP_REQUEST = ('GET', 'POST') # these kinds of requests won't be set in _method
    ANY_GET_REQUEST = ('GET',)
    USER_AGENT = "{0}/{1}".format(__project__, __version__)
    USER_AGENT_HEADER = {"User-Agent": USER_AGENT}

    def __init__(self, apikey, baseurl=None):
        """
            API Key required
            Baseurl default = http://api.semetric.com
        """
        self.apikey = apikey
        self.baseurl = (baseurl or self.API_BASE_URL).rstrip('/')
        self.http = httplib2.Http()

    @staticmethod
    def urlencode(qsdata):
        """
            URL Encode the params in a fixed order, sorted by key.
        """
        qsitems = sorted(qsdata.items(), key=itemgetter(0))
        return urlencode(qsitems)

    def _request(self, path, method='GET', **params):
        """
            Make an API request
        """
        base = "{0}/{1}".format(self.baseurl, path)
        # normalise the method argument
        method = method.upper().strip()

        # parse the existing url
        urlparts = urlparse(base)
        qstr = parse_qs(urlparts.query)

        # add the token to the query string
        qstr['token'] = self.apikey
        if method not in APIClient.HTTP_REQUEST:
            qstr['_method'] = method
        else:
            try:
                del qstr['_method']
            except KeyError:
                pass

        if method in APIClient.ANY_GET_REQUEST:
            # if it's a get request then update the query string with
            # the params
            qstr.update(params)
            # all of the params go in the query string
            query_string = APIClient.urlencode(qstr)
            # reconstruct the url
            url = urlunparse((urlparts.scheme,
                              urlparts.netloc,
                              urlparts.path,
                              urlparts.params,
                              query_string,
                              "")) # empty fragment
            log.debug("Making GET request to {0}".format(url))
            resp, content = self.http.request(url, "GET", headers=self.USER_AGENT_HEADER)
        else:
            # all of the params go in the query string
            query_string = APIClient.urlencode(qstr)
            # reconstruct the url
            url = urlunparse((urlparts.scheme,
                              urlparts.netloc,
                              urlparts.path,
                              urlparts.params,
                              query_string,
                              "")) # empty fragment
            log.debug("Making POST request to {0}".format(url))
            resp, content = self.http.request(url, "POST", urlencode(params), headers=self.USER_AGENT_HEADER)

        status = int(resp['status'])

        if status != 200:
            raise APIError("An unknown error occurred")

        return resp, json.loads(content)

    def request(self, path, **params):
        """
        """
        path = path.lstrip("/")
        reps, envelope = self._request(path, method="GET", **params)

        if envelope["success"]:
            response = envelope["response"]

            if isinstance(response, dict):
                return Entity(apisession=self, **response)
            elif isinstance(response, basestring):
                return response

        else:
            raise APIError(envelope["error"]["code"], envelope["error"]["msg"])

