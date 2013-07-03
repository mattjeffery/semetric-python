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

from semetric.apiclient.util import APIRelationship

# Special imports for Python 3
if sys.version_info >= (3,): # pragma: no cover
    xrange = range

log = logging.getLogger(__name__)

class Entity(object):
    """
        Base class for an entity in the Semetric API
    """
    __apiclass__ = "entity"
    __apiclass_plural__ = "entities"
    __subclass_mapping__ = None
    __primary_key__ = "id"
    __deferrable_properties__ = []

    def __new__(cls, apisession=None, supress_mapping_error=False, partial=False, **entity_dict):
        """
            Create a new class for the Entity being instantiated. The class of the object being created depends
            on the class variable passed to the __new__ method, we search the list of subclasses for this class
            and create a new class that has the corresponding __apiclass__ value. eg. The Artist class has
            __apiclass__ set to "artist" if we create an instance of Entity passing class="artist" then an
            instance of Artist will be returned with apisession set.
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
                apiclass = cls.__name__.lower()

        try:
            entity_class = subclasses[apiclass]
        except KeyError:
            entity_class = cls
            if not supress_mapping_error:
                warnings.warn("Could not map api class `{0}' to a python class".format(apiclass), stacklevel=2)

        # Create an instance of the class
        # Set the API Session internal variable for the entity
        new_entity_class = super(Entity, cls).__new__(entity_class)
        new_entity_class.__api_session__ = apisession
        new_entity_class.is_partial = partial


        # Find all the APIRelationships for this isntance.
        is_apirelationship = lambda x: isinstance(x, APIRelationship)
        for rname, relation in inspect.getmembers(new_entity_class, is_apirelationship):
            # Augment the APIRelationships with the parent class
            new_relation = relation.copy() # create a new instance of relation with the same settings
            setattr(new_entity_class, rname, new_relation)
            new_relation.parent = new_entity_class

        entity_mapping = Entity.subclass_mapping()

        # If the entity has properties that are the same name as api classes then build
        # API class instances for those objects.
        for EntitySubClass in entity_mapping.values():
            entity_name = EntitySubClass.__apiclass__

            if entity_dict.has_key(entity_name):
                setattr(new_entity_class, "_"+entity_name, EntitySubClass(**entity_dict[entity_name]))

        # Add the plural versions of the entities
        for EntitySubClass in entity_mapping.values():
            entity_name = EntitySubClass.__apiclass_plural__

            if entity_dict.has_key(entity_name) and type(entity_dict[entity_name]) is list:
                setattr(new_entity_class, "_"+entity_name, [ EntitySubClass(**e) for e in entity_dict[entity_name] ] )

        cls.subclass_mapping()

        return new_entity_class

    @staticmethod
    def list_subclasses(cls):
        """
            List all the subclasses of a class and any subclasses of those classes
        """
        for subclass in cls.__subclasses__():
            for subsubclass in Entity.list_subclasses(subclass):
                yield subsubclass

        if cls.__apiclass__:
            yield cls

    @classmethod
    def subclass_mapping(cls):
        """
            Generate a mapping from Semetric API classes to Python
            Classes and create a cache of the subclasses
        """
        if cls.__subclass_mapping__ is None:
            subclasses= dict((subclass.__apiclass__, subclass)
                              for subclass
                              in Entity.list_subclasses(cls))
            cls.__subclass_mapping__ = subclasses

        return cls.__subclass_mapping__

    @property
    def session(self):
        return self.__api_session__

    @property
    def clsname(self):
        return self.__apiclass__

    @property
    def clsname_plural(self):
        return self.__apiclass_plural__

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
        raise NotImplementedError

    def reload(self, **kwargs):
        """
            Reload the object from the API.
        """
        self.is_partial = False
        primary_key_val = getattr(self, self.__primary_key__)

        path, args = self.__apiget__(primary_key_val, **kwargs)
        new_self = self.session.request(path, **args)
        self.id = new_self.id
        self.extras = new_self.extras
        return new_self

    def __getattribute__(self, key):
        """
        """
        is_partial = object.__getattribute__(self, "is_partial")
        deferrable_properties = object.__getattribute__(self, "__deferrable_properties__")

        if key in deferrable_properties and is_partial:
            log.debug("Requesting a reload() for an entity, `{0}' not found".format(key))
            # Reload the API object
            entity_reload = object.__getattribute__(self, "reload")
            entity_reload()

        return object.__getattribute__(self, key)
