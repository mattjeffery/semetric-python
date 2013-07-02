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

class ReleaseGroup(Entity):
    __apiclass__ = "releasegroup"
    __apiclass_plural__ = "releasegroups"

    def __init__(self, id, name, **kwargs):
        self.id = id
        self.name = name

        self.extras = kwargs

    @property
    def artist(self):
        if self.artists and len(self.artists) > 0:
            return self.artists[0]
        else:
            return None

    @property
    def artists(self):
        """
            return the artists entities for this ReleaseGroup
        """
        if hasattr(self,"_artists"):
            return self._artists
