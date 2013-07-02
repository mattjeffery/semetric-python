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
import unittest2
from mock import patch

from semetric.apiclient import SemetricAPI
from semetric.apiclient.entity.base import Entity
from semetric.apiclient.entity.artist import Artist
from .consts import APIKEY

# Base string type for Python3
if sys.version_info >= (3,): # pragma: no cover
    basestring = str

class TestSemetricAPI(unittest2.TestCase):

    def test_search_request(self):

        api = SemetricAPI(APIKEY)

        # Make the api response
        with patch.object(api.client, 'request', autospec=True) as api_mock:
            api_mock.return_value = []
            api.search(Artist, name="lady gaga")

        api_mock.assert_called_once_with("artist", q="lady gaga")

    def test_get_request(self):

        api = SemetricAPI(APIKEY)

        # Make the api response
        with patch.object(api.client, 'request', autospec=True) as api_mock:
            api_mock.return_value = []
            api.get(Artist, id="foo")

        api_mock.assert_called_once_with("artist/foo")

    def test_search_request_not_implemented(self):

        api = SemetricAPI(APIKEY)
        with self.assertRaises(NotImplementedError) as exc:
            api.search(Entity, name="foo")

    def test_search_request_entity(self):

        api = SemetricAPI(APIKEY)

        # Make the api response
        with patch.object(api.client, 'request', autospec=True) as api_mock:
            api_mock.return_value = []
            api.get(Entity, id="foo")

        api_mock.assert_called_once_with("entity/foo")

