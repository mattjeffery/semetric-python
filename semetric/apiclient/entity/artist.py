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
"""
    .. module:: semetric.apiclient.entity.artist
"""
import logging

from semetric.apiclient.entity.base import Entity
from semetric.apiclient.entity.releasegroup import ReleaseGroup
from semetric.apiclient.entity.timeseries import DenseTimeseries
from semetric.apiclient.util import APIRelationship

log = logging.getLogger(__name__)


class Artist(Entity):
    """
        The :class:`Artist` entity represents the artists in the Semetric API.

        The :class:`Artist` entity supports the :func:`get()<semetric.apiclient.SemetricAPI.get>`
        and :func:`search()<semetric.apiclient.SemetricAPI.search>` methods of the
        :class:`SemetricAPI<semetric.apiclient.SemetricAPI>` class.
        To query the API for an Artist object the :func:`get()<semetric.apiclient.SemetricAPI.get>` method or
        the :func:`search()<semetric.apiclient.SemetricAPI.search>` method should be used.

        .. function:: SemetricAPI.get(entity, id[, idprefix=None])

            .. seealso:: This method refers to the :func:`SemetricAPI.get()<semetric.apiclient.SemetricAPI.get>` method.

            :param entity: the Artist entity class.
            :param id: ID of the Artist.
            :param idprefix: the prefix of the ID eg. `musicbrainz`.

            >>> semetricapi.get(Artist, id="fe66302b0aee49cfbd7d248403036def")
            >>> semetricapi.get(Artist, id="lady+gaga", idprefix="lastfm")

            TODO: full list of supported ID prefixes

        .. function:: SemetricAPI.search(entity, name)

            .. seealso:: This method refers to the :func:`SemetricAPI.search()<semetric.apiclient.SemetricAPI.search>` method.

            :param entity: the Artist entity class.
            :param name: Name of the artist to search for.

            >>> semetricapi.search(Artist, name="Lady Gaga")
            >>> semetricapi.search(Artist, name="Muse")


    """
    __apiclass__ = "artist"
    __apiclass_plural__ = "artists"
    __deferrable_properties__ = ["name"]

    releasegroups = APIRelationship(ReleaseGroup)

    def __init__(self, id, name=None, summary=None, **kwargs):
        self.id = id
        self.name = name
        self.summary = summary or {}
        self.extras = kwargs

    @classmethod
    def __apiget__(cls, id, idprefix=None):
        """
            Build a request for an Artist.

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

    def reload(self):
        """
            Reload the object from the API.
        """
        new_artist = super(Artist, self).reload()
        self.name = new_artist.name
        self.summary = new_artist.summary
        self.extras = new_artist.extras
        return new_artist

    def timeseries(self, dataset, **kwargs):
        """
            Get a Timeseries for an Artist.
        """
        path, args = DenseTimeseries.__apiget__(self, dataset, **kwargs)
        return self.session.request(path, **args)
