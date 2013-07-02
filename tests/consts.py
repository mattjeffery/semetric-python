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

try:
    import json
except ImportError: # pragma: no cover
    import simplejson as json

from semetric.apiclient.client import APIClient

APIKEY = "652a6295aebf4b6eba986dd1581f27f9" # random api key
EXPECT_USER_AGENT = {"User-Agent": APIClient.USER_AGENT}

ARTIST_ADELE_ID = "e6ee861435b24f67a6283e00bf820bab"
ARTIST_ADELE =   {"class": "artist",
                  "id": ARTIST_ADELE_ID,
                  "name": "Adele",
                  "summary": { "foo": "bar"},
                  "extra": True }

ARTIST_ADELE_WITH_RELEASEGROUPS = ARTIST_ADELE.copy()
ARTIST_ADELE_WITH_RELEASEGROUPS.update({"releasegroups": [{"class": "releasegroup", "name": "foo", "id": "foo"}],
                                        "releasegroup": {"class": "releasegroup", "name": "foo", "id": "foo"}})

ARTIST_ADELE_JSON = json.dumps({"response": ARTIST_ADELE,
                           "success": True })

UNKNOWN = {"class": "unknown"}

MOO_JSON = json.dumps({"response": "moooo",
                       "success": True })

ERROR_JSON = json.dumps({"error": { "msg": "Unknown Error", "code": 500 },
                         "success": False })

ARTIST_LIST = { "entities": [{ "class": "artist",
                               "id": "e78fc40de81a4e01babf1d23deaf2ca0",
                               "name": "50 Cent" }
                            ]}

DENSE_TIMESERIES = { "data": [1,2,3,4,5],
                     "period": 86400,
                     "start_time": 1258588800,
                     "end_time": 1258934400 }
