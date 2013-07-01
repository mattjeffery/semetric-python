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

class APIRelationship(object):
    """
        Define a relationship between to entities
    """

    def __init__(self, related_entity, *args, **kwargs):
        """
            Setup the relationship
        """
        self.related_entity = related_entity
        self._parent = None

    @property
    def parent(self):
        if self._parent is None:
            raise RuntimeError("parent must be set, has the class been setup correctly?")
        else:
            return self._parent


    @parent.setter
    def parent(self, parent):
        self._parent = parent

    def __call__(self):
        """
            Return the related entities from the API
        """

        path = "{cls}/{id}/{rel_cls}/".format(cls=self.parent.clsname,
                                              id=self.parent.id,
                                              rel_cls=self.related_entity.__apiclass__)

        return self.parent.session.request(path)
