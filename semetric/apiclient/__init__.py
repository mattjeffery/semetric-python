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
import os

def read(fname):
    """
        Utility function to read the README file, etc.
    """
    fh = None
    try:
        fh = open(os.path.join(os.path.dirname(__file__), fname))
    except:
        if fh:
            fh.close()
        raise
    return fh.read()

__project__ = "semetric-python"
__author__  = "Matt Jeffery <matt@clan.se>"
__version__ = read("VERSION.txt").strip() # stip any newlines etc

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

