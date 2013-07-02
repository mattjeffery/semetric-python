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
from semetric.apiclient.entity.base import Entity
from semetric.apiclient.entity.releasegroup import ReleaseGroup
from semetric.apiclient.util import APIRelationship
from .consts import (
    APIKEY,
    ARTIST_ADELE,
    ADELE_RELEASE_GROUP
)
# Base string type for Python3
if sys.version_info >= (3,): # pragma: no cover
    basestring = str

class TestMiscFunctions(unittest2.TestCase):

    def test_bad_setup(self):
        """
            Test that an incorrectly setup APIRelationship will fail with an exception
        """
        relationship = APIRelationship(Entity)
        with self.assertRaises(RuntimeError) as exc:
            relationship()

    def test_bad_setup_class(self):
        """
            Test that an incorrectly setup APIRelationship will fail with an exception
        """
        relationship = APIRelationship(object)
        with self.assertRaises(AttributeError) as exc:
            relationship()

    def test_list_relationship(self):
        """
            Test that an incorrectly setup APIRelationship will fail with an exception
        """
        relationship = APIRelationship(object)
        with self.assertRaises(AttributeError) as exc:
            relationship()

    def test_artist_relationship_with_list(self):
        apiclient = APIClient(APIKEY)

        # Make the api response
        with patch.object(apiclient, 'request', autospec=True) as api_mock:
            # Setup artist -> releasegroup relationship
            api_mock.return_value = [ReleaseGroup(**ADELE_RELEASE_GROUP)]
            a = Entity(apisession=apiclient, **ARTIST_ADELE)
            relationship = APIRelationship(ReleaseGroup, use_list=False)
            relationship.parent = a

            with warnings.catch_warnings(record=True) as w:
                # Cause all warnings to always be triggered.
                warnings.simplefilter("always")
                rg = relationship()

                assert len(w) == 1, "only one warning should have been generate"
                assert issubclass(w[-1].category, UserWarning), "a UserWarning should have been generated"
                assert "1:1 relationship" in str(w[-1].message), "The warning should tell the user about a non-1:1 relationship"
                assert isinstance(rg, ReleaseGroup), "a releasegroup should have been returned"

        api_mock.assert_called_once_with("artist/e6ee861435b24f67a6283e00bf820bab/releasegroup/")
