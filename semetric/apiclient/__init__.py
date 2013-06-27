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

import warnings

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

        apiclass = entity_dict.get('class', 'entity')
        try:
            entity_class = subclasses[apiclass]
        except KeyError:
            entity_class = Entity
            warnings.warn("Could not map api class `{0}' to a python class, using Entity".format(apiclass))

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



