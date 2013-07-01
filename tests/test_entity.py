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

import unittest2
import warnings
from mock import patch

from semetric.apiclient.entity import *

from .consts import ARTIST_ADELE, UNKNOWN, ARTIST_LIST, DENSE_TIMESERIES

class TestEntity(unittest2.TestCase):

    def test_entity_factory_artist(self):
        """
            Test creating an Entity from an entity dict
        """
        assert isinstance(Entity(**ARTIST_ADELE), Artist), "an Artist entity should be created"

    def test_entity_factory_blank(self):
        """
            Test creating an Entity from an empty dict
        """
        assert isinstance(Entity(), Entity), "a plain Entity should be created"

    def test_entity_factory_warning_unknown(self):
        """
            Test creating an Entity from an unknown entity dict
        """
        with warnings.catch_warnings(record=True) as w:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("always")
            # Trigger a warning.
            assert isinstance(Entity(**UNKNOWN), Entity), "a plain Entity should be created"
            # Verify some things
            assert len(w) == 1, "only one warning should have been generate"
            assert issubclass(w[-1].category, UserWarning), "a UserWarning should have been generated"
            assert "Could not map api" in str(w[-1].message), "The warning should tell the user than the api class cannot be mapped"

class TestListEntity(unittest2.TestCase):

    def test_entity_factory_artist(self):
        """
            Test creating an Entity from an entity dict
        """
        alist = Entity(**ARTIST_LIST)
        assert isinstance(alist, List), "a List entity should be created"
        assert len(alist) == 1, "the list should have one item in it"
        assert isinstance(alist[0], Artist), "the first item in the list should be an Artist"
        for item in alist:
            assert isinstance(item, Artist), "each item in the list should be an Artist"
        for item in alist[:]:
            assert isinstance(item, Artist), "each item in the slice should be an Artist"

class TestDenseEntity(unittest2.TestCase):

    def test_entity_factory_dense(self):
        """
            Test creating an Entity from an entity dict
        """
        timeseries = Entity(**DENSE_TIMESERIES)
        assert isinstance(timeseries, DenseTimeseries), "a DenseTimeseries entity should be created"
        assert len(timeseries) == 5, "the data should have 5 items in it"
        assert type(timeseries[0]) is tuple, "the data items should be tuples"

        # Test that the timestamps are calculated correctly
        expected_timestamp = timeseries.start_time
        for timestamp, data in timeseries:
            assert timestamp == expected_timestamp, "expected time stamp does not match"
            expected_timestamp += timeseries.period
        # Make sure the end_time is correct
        assert timeseries.end_time == timestamp, "expected end time stamp does not match last time stamp"
