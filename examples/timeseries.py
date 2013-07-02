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
import csv
import sys

from datetime import datetime
from argparse import ArgumentParser

from semetric.apiclient import SemetricAPI
from semetric.apiclient.entity.artist import Artist

log = logging.getLogger(__name__)

if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument('--apikey', type=str, help='your semetric api key')
    parser.add_argument('--no-header', action="store_true", help='disable the header for the csv file')
    parser.add_argument('--unix-timestamp', action="store_true", help='leave the timestamps as unix epoch time', default=False)
    parser.add_argument('--country', type=str, help='country iso code for the time series')
    parser.add_argument('--variant', type=str, help='variant for the timeseries [default=diff]')
    parser.add_argument('--processing', type=str, help='processing level for the timeseries [default=processed]')
    parser.add_argument('--granularity', type=str, help='granularity for the timeseries [default=day]')
    parser.add_argument('artist_id', type=str, help='name of the artist to find')
    parser.add_argument('dataset', type=str, help='dataset to get the data for')
    args = parser.parse_args()

    if args.apikey is None:
        parser.error("an API key must be provided")

    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s %(message)s')

    api = SemetricAPI(args.apikey)

    log.debug("Loading artist with ID: {0}".format(args.artist_id))

    artist = api.get(Artist, id=args.artist_id)

    csvout = csv.writer(sys.stdout, delimiter='\t')
    if not args.no_header:
        csvout.writerow(["timestamp", "value"])

    for ts, value in artist.timeseries(args.dataset, variant=args.variant, processing=args.processing, country=args.country, granularity=args.granularity):
        if args.unix_timestamp:
            timestamp = ts
        else:
            dt = datetime.utcfromtimestamp(ts)
            timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")
        csvout.writerow([timestamp, value])