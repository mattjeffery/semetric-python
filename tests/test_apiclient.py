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
import warnings
from mock import patch

from semetric.apiclient.client import APIClient
from semetric.apiclient.exc import APIError
from semetric.apiclient.entity import Artist

from .consts import (
    APIKEY,
    EXPECT_USER_AGENT,
    ARTIST_ADELE_JSON,
    ARTIST_ADELE_ID,
    MOO_JSON,
    ERROR_JSON
)

# Base string type for Python3
if sys.version_info >= (3,): # pragma: no cover
    basestring = str

class TestAPIClient(unittest2.TestCase):

    def test_bad_repsonse(self):

        apiclient = APIClient(APIKEY)

        # Make the api response
        with patch.object(apiclient.http, 'request', autospec=True) as api_mock:
            api_mock.return_value = ({'status': 500}, "")

            # Make sure an APIError is raise on non-200 respsonse
            with self.assertRaises(APIError):
                apiclient._request("moo")

        api_mock.assert_called_once_with("http://api.semetric.com/moo?token={0}".format(APIKEY),
                                         "GET",
                                         headers=EXPECT_USER_AGENT)

    def test_get_request(self):
        """
            Test that a GET request is made an behaves as expected
        """

        apiclient = APIClient(APIKEY)

        # Make the api response
        with patch.object(apiclient.http, 'request', autospec=True) as api_mock:
            api_mock.return_value = ({'status': 200}, "{}")
            apiclient._request("moo")

        api_mock.assert_called_once_with("http://api.semetric.com/moo?token={0}".format(APIKEY),
                                         "GET",
                                         headers=EXPECT_USER_AGENT)

    def test_post_request(self):
        """
            Test that a POST request is made an behaves as expected
        """

        apiclient = APIClient(APIKEY)

        # Make the api response
        with patch.object(apiclient.http, 'request', autospec=True) as api_mock:
            api_mock.return_value = ({'status': 200}, "{}")
            apiclient._request("moo", method="POST")

        api_mock.assert_called_once_with("http://api.semetric.com/moo?token={0}".format(APIKEY),
                                         "POST",
                                         "", # no data
                                         headers=EXPECT_USER_AGENT)

    def test_put_request(self):
        """
            Test that a PUT request is made an behaves as expected
        """

        apiclient = APIClient(APIKEY)

        # Make the api response
        with patch.object(apiclient.http, 'request', autospec=True) as api_mock:
            api_mock.return_value = ({'status': 200}, "{}")
            apiclient._request("moo", method="PUT")

        api_mock.assert_called_once_with("http://api.semetric.com/moo?_method=PUT&token={0}".format(APIKEY),
                                         "POST",
                                         "", # no data
                                         headers=EXPECT_USER_AGENT)

    def test_artist_request(self):
        """
            Test that an Artist entity is correctly parsed by the API
            client
        """

        apiclient = APIClient(APIKEY)

        # Make the api response
        with patch.object(apiclient.http, 'request', autospec=True) as api_mock:
            api_mock.return_value = ({'status': 200}, ARTIST_ADELE_JSON)
            resp = apiclient.request("/artist/"+ARTIST_ADELE_ID)
            assert isinstance(resp, Artist)
            # check the session is set correctly
            assert resp.session == apiclient

        api_mock.assert_called_once_with("http://api.semetric.com/artist/{0}?token={1}".format(ARTIST_ADELE_ID, APIKEY),
                                         "GET",
                                         headers=EXPECT_USER_AGENT)

    def test_moo_request(self):
        """
            Test that an Artist entity is correctly parsed by the API
            client
        """

        apiclient = APIClient(APIKEY)

        # Make the api response
        with patch.object(apiclient.http, 'request', autospec=True) as api_mock:
            api_mock.return_value = ({'status': 200}, MOO_JSON)
            resp = apiclient.request("/moo")
            assert isinstance(resp, basestring)

        api_mock.assert_called_once_with("http://api.semetric.com/moo?token={0}".format(APIKEY),
                                         "GET",
                                         headers=EXPECT_USER_AGENT)

    def test_bad_request(self):
        """
            Test that an Artist entity is correctly parsed by the API
            client
        """

        apiclient = APIClient(APIKEY)

        # Make the api response
        with patch.object(apiclient.http, 'request', autospec=True) as api_mock:
            api_mock.return_value = ({'status': 200}, ERROR_JSON)
            try:
                apiclient.request("/error")
            except APIError as apierror:
                errcode, errmsg = apierror.args
                assert errcode == 500
                assert "Error" in errmsg
            else:
                assert False, "APIError exception was not raised"


        api_mock.assert_called_once_with("http://api.semetric.com/error?token={0}".format(APIKEY),
                                         "GET",
                                         headers=EXPECT_USER_AGENT)
