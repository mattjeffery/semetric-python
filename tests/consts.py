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

from semetric.apiclient import APIClient

APIKEY = "652a6295aebf4b6eba986dd1581f27f9" # random api key
EXPECT_USER_AGENT = {"User-Agent": APIClient.USER_AGENT}

ARTIST_ADELE = {"class": "artist",
                "id": "e6ee861435b24f67a6283e00bf820bab",
                "name": "Adele" }
UNKNOWN = {"class": "unknown"}
