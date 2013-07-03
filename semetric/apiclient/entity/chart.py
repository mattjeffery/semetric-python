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
    __deferrable_properties__ = ["name", "data", "period", "end_time", "data", "name", "now_id", "start_time", "previous_id", "chart_items"]

    def __init__(self, id, country='ALL', data=None, period=None, end_time=None, name=None, now_id=None, start_time=None, previous_id=None, **kwargs):

        self.id = id
        self.name = name
        self.data = data
        self.period= period
        self.end_time = end_time
        self.data = data
        self.name = name
        self.now_id = now_id
        self.start_time = start_time
        self.previous_id = previous_id
        self.country = country
        self.chart_items = map(lambda x: ChartItem(supress_mapping_error=True, **x), self.data or [])

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

    def reload(self):
        """
            Reload the Chart entity from the API
        """
        new_chart = super(Chart, self).reload(country=self.country)
        self.name = new_chart.name
        self.data = new_chart.data
        self.period = new_chart.period
        self.end_time = new_chart.end_time
        self.data = new_chart.data
        self.name = new_chart.name
        self.now_id = new_chart.now_id
        self.start_time = new_chart.start_time
        self.previous_id = new_chart.previous_id
        self.chart_items = map(lambda x: ChartItem(supress_mapping_error=True, **x), self.data or [])

    @classmethod
    def __apiget__(cls, id, country=None):
        """
            Get the chart from the API by ID
        """
        path = "{entity}/{id}".format(entity=cls.__apiclass__, id=id)
        args = { 'country': country or 'ALL' }
        return path, args
