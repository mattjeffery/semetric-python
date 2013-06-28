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

import unittest2
import warnings
from mock import patch

from semetric.apiclient import APIClient, APIError

from consts import APIKEY, EXPECT_USER_AGENT

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
