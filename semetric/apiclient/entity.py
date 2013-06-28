#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Copyright (C) 2013  Matt Jeffery <matt@clan,se>
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
import warnings

__all__ = ['Entity', 'Artist', 'List']

# Special imports for Python 3
if sys.version_info >= (3,): # pragma: no cover
    xrange = range

class Entity(object):
    """
        Base class for an entity in the Semetric API
    """
    __apiclass__ = "entity"

    @staticmethod
    def subclass_mapping():
        """
            Generate a mapping from Semetric API classes to Python
            Classes.
        """
        subclasses= dict((subclass.__apiclass__, subclass)
                         for subclass
                         in Entity.__subclasses__())
        subclasses['entity'] = Entity
        return subclasses

    @staticmethod
    def entity_factory(entity_dict):
        subclasses = Entity.subclass_mapping()

        apiclass = entity_dict.get('class')

        if apiclass is None:
            # special cases for lists, timeseries, etc.
            if 'entities' in entity_dict: # list
                apiclass = "list"
            elif 'data' in entity_dict: # time series
                apiclass = 'dense'
            else: # fall back
                apiclass = 'entity'

        try:
            entity_class = subclasses[apiclass]
        except KeyError:
            entity_class = Entity
            warnings.warn("Could not map api class `{0}' to a python class, using Entity".format(apiclass), stacklevel=2)

        return entity_class(**entity_dict)

    def __init__(self, **kwargs):
        """
            Set up some basics for an Entity
        """
        pass

class Artist(Entity):
    __apiclass__ = "artist"

    def __init__(self, id, name, **kwargs):
        self.id = id
        self.name = name
        self.extras = kwargs

class List(Entity):
    __apiclass__ = "list"

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
            return map(Entity.entity_factory, self.entities[index])
        else:
            return Entity.entity_factory(self.entities[index])

    def __iter__(self):
        """
            Simple iterator
        """
        for i in xrange(len(self)):
            yield self[i]
