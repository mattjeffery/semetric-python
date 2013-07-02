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


class ChartItem(Entity):
    """
        A ChartItem represents an item in a chart, each chart item is an entity, for legacy
        reasons a chart can have multiple entity types, eg. a release group chart will have
        the expected releasegroup entity and an artist entity as well.

        All chart items have `rank` and `value` properties.
    """
    __apiclass__ = None
    __apiclass_plural__ = None

    def __init__(self, rank, value, **chartitem):
        """
            Create an instance of ChartItem
        """
        # parse the chart item
        self.rank = rank
        self.value = value

class Chart(Entity):
    """
        A chart is a rank list of entities.
    """
    __apiclass__ = "chart"
    __apiclass_plural__ = "charts"

    def __init__(self, data, period, end_time, name, now_id, start_time, previous_id, **kwargs):

        self.id = None
        self.name = None
        self.data = data
        self.period= period
        self.end_time = end_time
        self.data = data
        self.name = name
        self.now_id = now_id
        self.start_time = start_time
        self.previous_id = previous_id
        self.chart_items = map(lambda x: ChartItem(supress_mapping_error=True, **x), self.data)

        self.extras = kwargs

    def __len__(self):
        """
            Get the length of the chart
        """
        return len(self.data)

    def __getitem__(self, index):
        """
            Get an item or item slice from the chart
        """
        return self.chart_items[index]

    def __iter__(self):
        """
            Simple iterator
        """
        for i in xrange(len(self)):
            yield self[i]

    @classmethod
    def __apiget__(cls, id, country=None):
        """
            Get the chart from the API by ID
        """
        path = "{entity}/{id}".format(entity=cls.__apiclass__, id=id)
        args = { 'country': country or 'ALL' }
        return path, args
