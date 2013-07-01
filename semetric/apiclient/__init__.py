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

__project__ = "semetric-python"
__author__  = "Matt Jeffery <matt@clan.se>"
__status__  = "alpha"
__version_major__ = 0
__version_minor__ = 1
__version_patch__ = 0
__version__ = "{major}.{minor}.{patch}".format(major=__version_major__,
                                               minor=__version_minor__,
                                               patch=__version_patch__)

from semetric.apiclient.client import APIClient

class SemetricAPI(object):
    def __init__(self, apikey, baseurl=None):
        """
            foo
        """
        self.client = APIClient(apikey, baseurl)

    def get(self, entity, eid):

        path = "{0}/{1}".format(entity.__apiclass__, eid)

        return self.client.request(path)

    def search(self, entity, name):

        path = "{0}".format(entity.__apiclass__)

        return self.client.request(path, q=name)

