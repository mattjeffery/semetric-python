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

import logging

from semetric.apiclient.entity.base import Entity

log = logging.getLogger(__name__)

class DenseTimeseries(Entity):
    __apiclass__ = "dense"

    def __init__(self, data, start_time, end_time, period, **kwargs):
        self.id = None
        self.name = None

        self.start_time = start_time
        self.end_time = end_time
        self.period = period
        # original and processed data
        self._data = data
        self.data = self._timeseries(self._data)
        self.extras = kwargs

    def _timeseries(self, data):
        """
            Generate the timeseries data
        """
        return list(zip(range(self.start_time, self.end_time+self.period, self.period), data))

    def __len__(self):
        """
            Get the length of the data
        """
        return len(self.data)

    def __getitem__(self, index):
        """
            Get an item or item slice from the data
        """
        return self.data[index]

    def __iter__(self):
        """
            Simple iterator for the data
        """
        for i in xrange(len(self)):
            yield self[i]
