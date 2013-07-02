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

from semetric.apiclient.entity.base import Entity
from semetric.apiclient.util import APIRelationship

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
