#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

__project__ = "semetric-python"
__author__  = "Matt Jeffery <matt@clan.se>"
__status__  = "alpha"
__version__ = "0.1.0"

import sys
import warnings
import httplib2

# Special imports for Python 3
if sys.version_info >= (3,): # pragma: no cover
    from urllib.parse import urlparse, urlunparse, urlencode, parse_qs
else: # pragma: no cover
    from urllib import urlencode
    from urlparse import urlparse, urlunparse, parse_qs

try:
    import json
except ImportError: # pragma: no cover
    import simplejson as json

from operator import itemgetter

class APIError(Exception):
    pass

class APIClient(object):
    """
        API Client
    """

    API_BASE_URL = "http://api.semetric.com"
    HTTP_REQUEST = ('GET', 'POST') # these kinds of requests won't be set in _method
    ANY_GET_REQUEST = ('GET',)
    USER_AGENT = "{0}/{1}".format(__project__, __version__)
    USER_AGENT_HEADER = {"User-Agent": USER_AGENT}

    def __init__(self, apikey, baseurl=API_BASE_URL):
        self.apikey = apikey
        self.baseurl = baseurl.rstrip('/')
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
            resp, content = self.http.request(url, "POST", urlencode(params), headers=self.USER_AGENT_HEADER)

        status = int(resp['status'])

        if status != 200:
            raise APIError("An unknown error occurred")

        return resp, json.loads(content)

    def __call__(self, path):
        pass

class Entity(object):
    """
        Base class for an entity in the Semetric API
    """
    __apiclass__ = "entity"

    @staticmethod
    def subclass_mapping():
        """
            Generate a mapping from Semetric API classes to Python
            Classes.
        """
        subclasses= dict((subclass.__apiclass__, subclass)
                         for subclass
                         in Entity.__subclasses__())
        subclasses['entity'] = Entity
        return subclasses

    @staticmethod
    def entity_factory(entity_dict):
        subclasses = Entity.subclass_mapping()

        apiclass = entity_dict.get('class', 'entity')
        try:
            entity_class = subclasses[apiclass]
        except KeyError:
            entity_class = Entity
            warnings.warn("Could not map api class `{0}' to a python class, using Entity".format(apiclass), stacklevel=2)

        return entity_class(**entity_dict)

    def __init__(self, **kwargs):
        """
            Set up some basics for an Entity
        """
        pass

class Artist(Entity):
    __apiclass__ = "artist"

    def __init__(self, id, name, **kwargs):
        self.id = id
        self.name = name
        self.extras = kwargs



