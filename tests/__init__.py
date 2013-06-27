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
import semetric.apiclient

class TestEntity(unittest2.TestCase):

    def test_factory(self):
        """
            Test creating an Entity from an entity dict
        """
        artist_dict = {"class": "artist",
                       "id": "e6ee861435b24f67a6283e00bf820bab",
                       "name": "Adele" }
        entity = semetric.apiclient.Entity.entity_factory(artist_dict)
        assert isinstance(entity, semetric.apiclient.Artist), "an Artist entity should be created"

        assert isinstance(semetric.apiclient.Entity.entity_factory({}), semetric.apiclient.Entity), "a blank Entity should be created"

if __name__ == '__main__':
    unittest2.main()

