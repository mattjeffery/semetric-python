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

from semetric.apiclient import Entity, Artist

class TestEntity(unittest2.TestCase):

    ADELE = {"class": "artist",
             "id": "e6ee861435b24f67a6283e00bf820bab",
             "name": "Adele" }
    UNKNOWN = {"class": "unknown"}
    BLANK = {}

    def test_entity_factory_artist(self):
        """
            Test creating an Entity from an entity dict
        """
        assert isinstance(Entity.entity_factory(self.ADELE), Artist), "an Artist entity should be created"

    def test_entity_factory_blank(self):
        """
            Test creating an Entity from an entity dict
        """
        assert isinstance(Entity.entity_factory(self.BLANK), Entity), "a plain Entity should be created"

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

if __name__ == '__main__':
    unittest2.main()

