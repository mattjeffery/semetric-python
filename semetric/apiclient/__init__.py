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
"""
    A wrapper for the Semetric (and Musicmetric) API.

    The :class:`SemetricAPI` is the main entry point for interacting the with
    Semetric API::

        >>> from semetric.apiclient import SemetricAPI
        >>> from semetric.apiclient.entity import Artist

        >>> semetricapi = SemetricAPI(apitoken)
        >>> artist = semetricapi.get(Artist, id="fe66302b0aee49cfbd7d248403036def")
        >>> artist.name
        "Lady Gaga"

    .. moduleauthor:: Matt Jeffery <matt@clan.se>

"""

import os

def read(fname):
    """
        Utility function to read the README file, etc.
    """
    fh = None
    try:
        fh = open(os.path.join(os.path.dirname(__file__), fname))
    except: # pragma: no cover
        if fh:
            fh.close()
        raise
    return fh.read()

__project__ = "semetric-python"
__author__  = "Matt Jeffery <matt@clan.se>"
__version__ = "0.2.1"

from semetric.apiclient.client import APIClient

class SemetricAPI(object):
    """
        The main API wrapper class for the Semetric API.
    """
    def __init__(self, apikey, baseurl=None):
        """
            :param apikey: Your Semetric API key.
            :type apikey: str
            :param baseurl: the api instance to use.
            :default baseurl: http://api.semetric.com
            :type baseurl: str
        """
        self.client = APIClient(apikey, baseurl)

    def get(self, entity, **kwargs):
        """
            Query the API to get an Entity from the API based on id
            params.

            :param entity: The entity type to query.
            :type entity: :class:`semetric.apiclient.entity.Entity`
            :param kwargs: extra arguments depending on the entity type.
            :type kwargs: kwargs
            :returns: :class:`semetric.apiclient.entity.Entity` -- the result from the query.
            :raises: :class:`semetric.apiclient.exc.APIError`

        """
        # TODO: inspect apiget for arguments
        path, args = entity.__apiget__(**kwargs)
        return self.client.request(path, **args)

    def search(self, entity, **kwargs):
        """
            Search for Entities in using the API

            :param entity: The entity type to query.
            :type entity: :class:`semetric.apiclient.entity.Entity`
            :param kwargs: extra arguments depending on the entity type.
            :type kwargs: kwargs
            :returns: :class:`semetric.apiclient.entity.Entity` -- the result from the query.
            :raises: :class:`semetric.apiclient.exc.APIError`
        """
        path, args = entity.__apisearch__(**kwargs)
        return self.client.request(path, **args)
