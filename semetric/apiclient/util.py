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
import warnings
import logging

log = logging.getLogger(__name__)

class APIRelationship(object):
    """
        Define a relationship between to entities
    """

    def __init__(self, related_entity, use_list=True, *args, **kwargs):
        """
            Setup the relationship
        """
        self.related_entity = related_entity
        self.use_list = use_list
        self._parent = None

    def copy(self):
        relation = APIRelationship(self.related_entity)
        relation._parent = self._parent
        return relation

    @property
    def parent(self):
        if self._parent is None:
            raise RuntimeError("parent must be set, has the class been setup correctly?")
        else:
            return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent

    @property
    def related_entity_name(self):
        return "_"+(self.related_entity.__apiclass_plural__ if self.use_list else self.related_entity.__apiclass__)

    def __call__(self):
        """
            Return the related entities from the API
        """
        relation_attr = self.related_entity_name
        if not hasattr(self.parent, relation_attr) or getattr(self.parent, relation_attr) is None:
            path = "{cls}/{id}/{rel_cls}/".format(cls=self.parent.clsname,
                                                  id=self.parent.id,
                                                  rel_cls=self.related_entity.__apiclass__)
            reply = self.parent.session.request(path)
            if self.use_list:
                if type(reply) is list:
                    setattr(self.parent, relation_attr, reply)
                else:
                    # for the relationship in to a list
                    setattr(self.parent, relation_attr, [reply])
            else:
                if type(reply) is list:
                    # force the relationship out of a list and raise a warning
                    warnings.warn("relationship was not expecting a list result, perhaps this is no a 1:1 relationship", stacklevel=2)
                    setattr(self.parent, relation_attr, reply[0] if len(reply) > 0 else None)
                else:
                    setattr(self.parent, relation_attr, reply)

        return getattr(self.parent, relation_attr)
