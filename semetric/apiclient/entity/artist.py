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
from semetric.apiclient.entity.releasegroup import ReleaseGroup
from semetric.apiclient.util import APIRelationship

log = logging.getLogger(__name__)


class Artist(Entity):
    __apiclass__ = "artist"
    __apiclass_plural__ = "artists"

    releasegroups = APIRelationship(ReleaseGroup)

    def __init__(self, id, name, summary=None, **kwargs):
        self.id = id
        self.name = name
        self.summary = summary or {}
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
