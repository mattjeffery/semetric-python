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

from semetric.apiclient import Entity, Artist, APIClient, APIError

class TestEntity(unittest2.TestCase):

    ADELE = {"class": "artist",
             "id": "e6ee861435b24f67a6283e00bf820bab",
             "name": "Adele" }
    UNKNOWN = {"class": "unknown"}

    def test_entity_factory_artist(self):
        """
            Test creating an Entity from an entity dict
        """
        assert isinstance(Entity.entity_factory(self.ADELE), Artist), "an Artist entity should be created"

    def test_entity_factory_blank(self):
        """
            Test creating an Entity from an empty dict
        """
        assert isinstance(Entity.entity_factory({}), Entity), "a plain Entity should be created"

    def test_entity_factory_warning_unknown(self):
        """
            Test creating an Entity from an unknown entity dict
        """
        with warnings.catch_warnings(record=True) as w:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("always")
            # Trigger a warning.
            assert isinstance(Entity.entity_factory(self.UNKNOWN), Entity), "a plain Entity should be created"
            # Verify some things
            assert len(w) == 1, "only one warning should have been generate"
            assert issubclass(w[-1].category, UserWarning), "a UserWarning should have been generated"
            assert "Could not map api" in str(w[-1].message), "The warning should tell the user than the api class cannot be mapped"

class TestAPIClient(unittest2.TestCase):

    APIKEY = "652a6295aebf4b6eba986dd1581f27f9" # random api key
    EXPECT_USER_AGENT = {"User-Agent": APIClient.USER_AGENT}

    def test_bad_repsonse(self):

        apiclient = APIClient(self.APIKEY)

        # Make the api response
        with patch.object(apiclient.http, 'request', autospec=True) as api_mock:
            api_mock.return_value = ({'status': 500}, "")

            # Make sure an APIError is raise on non-200 respsonse
            with self.assertRaises(APIError):
                apiclient._request("moo")

        api_mock.assert_called_once_with("http://api.semetric.com/moo?token={0}".format(self.APIKEY),
                                         "GET",
                                         headers=self.EXPECT_USER_AGENT)

    def test_get_request(self):
        """
            Test that a GET request is made an behaves as expected
        """

        apiclient = APIClient(self.APIKEY)

        # Make the api response
        with patch.object(apiclient.http, 'request', autospec=True) as api_mock:
            api_mock.return_value = ({'status': 200}, "{}")
            apiclient._request("moo")

        api_mock.assert_called_once_with("http://api.semetric.com/moo?token={0}".format(self.APIKEY),
                                         "GET",
                                         headers=self.EXPECT_USER_AGENT)

    def test_post_request(self):
        """
            Test that a POST request is made an behaves as expected
        """

        apiclient = APIClient(self.APIKEY)

        # Make the api response
        with patch.object(apiclient.http, 'request', autospec=True) as api_mock:
            api_mock.return_value = ({'status': 200}, "{}")
            apiclient._request("moo", method="POST")

        api_mock.assert_called_once_with("http://api.semetric.com/moo?token={0}".format(self.APIKEY),
                                         "POST",
                                         "", # no data
                                         headers=self.EXPECT_USER_AGENT)


if __name__ == '__main__':
    unittest2.main()

