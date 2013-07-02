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

class List(Entity):
    __apiclass__ = "list"
    __apiclass_plural__ = "lists"

    def __init__(self, entities, **kwargs):
        self.id = None
        self.name = None
        self.entities = entities
        self.extras = kwargs

    def __len__(self):
        """
            Get the length of the list
        """
        return len(self.entities)

    def __getitem__(self, index):
        """
            Get an item or item slice from the list
        """
        if isinstance(index, slice):
            # return the entity_factory results for each item in the
            # slice
            return map(lambda x: Entity(**x), self.entities[index])
        else:
            return Entity(**self.entities[index])

    def __iter__(self):
        """
            Simple iterator
        """
        for i in xrange(len(self)):
            yield self[i]
