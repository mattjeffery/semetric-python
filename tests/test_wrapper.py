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
from semetric.apiclient.exc import APIError
from semetric.apiclient.entity.base import Entity
from semetric.apiclient.entity.artist import Artist
from semetric.apiclient.entity.chart import Chart
from .consts import (
    APIKEY,
    ARTIST_ADELE,
    ARTIST_ADELE_ID
)

# Base string type for Python 3
if sys.version_info >= (3,): # pragma: no cover
    basestring = str

class TestSemetricAPI(unittest2.TestCase):

    def test_get_request_bad(self):

        api = SemetricAPI(APIKEY)

        # Make the api response
        with patch.object(api.client, 'request', autospec=True) as api_mock:
            api_mock.return_value = ""
            with self.assertRaises(APIError):
                api.get(Artist, name="lady gaga")

    def test_search_request_artist(self):

        api = SemetricAPI(APIKEY)

        # Make the api response
        with patch.object(api.client, 'request', autospec=True) as api_mock:
            api_mock.return_value = []
            api.search(Artist, name="lady gaga")

            api_mock.assert_called_once_with("artist", q="lady gaga")

    def test_get_request_artist(self):

        api = SemetricAPI(APIKEY)

        # Make the api response
        with patch.object(api.client, 'request', autospec=True) as api_mock:
            # Setup the API response
            api_mock.return_value = Artist(apisession=api.client, id="87e0e4ccc7f4415cbd6ba60ad49943b6")
            a = api.get(Artist, id="87e0e4ccc7f4415cbd6ba60ad49943b6")
            assert not api_mock.called, "the API should only be called when accessing a property that isn't cached"

            # The API should only be called if an unknown value is accessed
            a.name
            api_mock.assert_called_once_with("artist/87e0e4ccc7f4415cbd6ba60ad49943b6")

    def test_search_request_not_implemented(self):

        api = SemetricAPI(APIKEY)
        with self.assertRaises(NotImplementedError):
            api.search(Entity, name="foo")

    def test_search_request_entity(self):

        api = SemetricAPI(APIKEY)

        # Make the api response
        with patch.object(api.client, 'request', autospec=True) as api_mock:
            api_mock.return_value = Entity(apisession=api.client, id="87e0e4ccc7f4415cbd6ba60ad49943b6")
            api.get(Entity, id="87e0e4ccc7f4415cbd6ba60ad49943b6")
            assert not api_mock.called, "the API should only be called when accessing a property that isn't cached"

    def test_get_chart_with_country(self):

        api = SemetricAPI(APIKEY)

        # Make the api response
        with patch.object(api.client, 'request', autospec=True) as api_mock:
            api_mock.return_value = Chart(apisession=api.client, id="0695f0bba6144dfaa390e9b9f017ceab", country="CA")
            api.get(Chart, id="0695f0bba6144dfaa390e9b9f017ceab", country="CA")

            api_mock.assert_called_once_with("chart/0695f0bba6144dfaa390e9b9f017ceab", country="CA")

    def test_get_chart_without_country(self):

        api = SemetricAPI(APIKEY)

        # Make the api response
        with patch.object(api.client, 'request', autospec=True) as api_mock:
            api_mock.return_value = Chart(apisession=api.client, id="0695f0bba6144dfaa390e9b9f017ceab")
            api.get(Chart, id="0695f0bba6144dfaa390e9b9f017ceab")

            api_mock.assert_called_once_with("chart/0695f0bba6144dfaa390e9b9f017ceab", country="ALL")

    def test_get_artist_timeseries(self):

        api = SemetricAPI(APIKEY)

        # Make the api response
        with patch.object(api.client, 'request', autospec=True) as api_mock:
            api_mock.return_value = Entity(apisession=api.client, **ARTIST_ADELE)
            artist = api.get(Artist, id=ARTIST_ADELE_ID)

            assert isinstance(artist, Artist)
            assert not api_mock.called, "the API should only be called when accessing a property that isn't cached"

            artist.timeseries("plays/total")
            api_mock.assert_called_once_with("artist/e6ee861435b24f67a6283e00bf820bab/plays/total",
                                             country="ALL",
                                             variant="diff",
                                             processing="processed",
                                             granularity="day")
