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
import warnings
import logging
import inspect

__all__ = ['Entity', 'Artist', 'List', 'DenseTimeseries']

# Special imports for Python 3
if sys.version_info >= (3,): # pragma: no cover
    xrange = range

from semetric.apiclient.util import APIRelationship

log = logging.getLogger(__name__)

class Entity(object):
    """
        Base class for an entity in the Semetric API
    """
    __apiclass__ = "entity"

    def __new__(cls, apisession=None, **entity_dict):
        """
            Create a new class for the Entity being instantiated.
            The class of the object being created depends on the class
            variable passed to the __new__ method, we search the list
            of subclasses for this class and create a new class that
            has the corresponding __apiclass__ value. eg. The Artist
            class has __apiclass__ set to "artist" if we create an
            instance of Entity passing class="artist" then an instance
            of Artist will be returned with apisession set.

        """
        subclasses = cls.subclass_mapping()

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
            entity_class = cls
            warnings.warn("Could not map api class `{0}' to a python class, using Entity".format(apiclass), stacklevel=2)

        # Create an instance of the class
        # Set the API Session internal variable for the entity
        new_entity_class = super(Entity, cls).__new__(entity_class) #, apisession=apisession, **entity_dict)
        new_entity_class.__api_session__ = apisession


        # Find all the APIRelationships for this isntance.
        is_apirelationship = lambda x: isinstance(x, APIRelationship)
        for rname, relation in inspect.getmembers(new_entity_class, is_apirelationship):
            # Augment the APIRelationships with the parent class
            relation.parent = new_entity_class

        return new_entity_class

    @classmethod
    def subclass_mapping(cls):
        """
            Generate a mapping from Semetric API classes to Python
            Classes.
        """
        subclasses= dict((subclass.__apiclass__, subclass)
                         for subclass
                         in cls.__subclasses__())
        subclasses['entity'] = cls
        return subclasses

    @property
    def session(self):
        return self.__api_session__

    @property
    def clsname(self):
        return self.__apiclass__

    def __init__(self, **kwargs):
        """
            Set up some basics for an Entity
        """
        pass

    @classmethod
    def __apiget__(cls, id):
        """
            API ID
        """
        path = "{entity}/{id}".format(entity=cls.__apiclass__, id=id)
        return path, {}

    @classmethod
    def __apisearch__(cls, name):
        """

        """
        raise NotImplementedError

class ReleaseGroup(Entity):
    __apiclass__ = "releasegroup"

    def __init__(self, id, name, **kwargs):
        self.id = id
        self.name = name
        self.extras = kwargs

class Artist(Entity):
    __apiclass__ = "artist"

    releasegroups = APIRelationship(ReleaseGroup)

    def __init__(self, id, name, **kwargs):
        self.id = id
        self.name = name
        self.extras = kwargs

    @classmethod
    def __apiget__(cls, id, idprefix=None):
        """
            API ID
        """
        api_id = "{0}:{1}".format(idprefix, id) if idprefix else id
        path = "{entity}/{id}".format(entity=cls.__apiclass__,
                                      id=api_id)
        args = {}
        return path, args

    @classmethod
    def __apisearch__(cls, name):
        """
        """
        return cls.__apiclass__, {"q": name}

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
            return map(lambda x: Entity(**x), self.entities[index])
        else:
            return Entity(**self.entities[index])

    def __iter__(self):
        """
            Simple iterator
        """
        for i in xrange(len(self)):
            yield self[i]

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
