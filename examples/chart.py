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

from argparse import ArgumentParser

from semetric.apiclient import SemetricAPI
from semetric.apiclient.entity.chart import Chart

log = logging.getLogger(__name__)

if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument('--apikey', type=str, help='you semetric api key')
    parser.add_argument('--country', type=str, help='country iso code for the chart')
    parser.add_argument('--no-header', action="store_true", help='disable the header for the csv file')
    parser.add_argument('chart_id', type=str, help='id of the chart')
    args = parser.parse_args()

    if args.apikey is None:
        parser.error("an API key must be provided")

    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s %(message)s')

    api = SemetricAPI(args.apikey)

    log.debug("Loading chart with ID: {0}".format(args.chart_id))

    chart = api.get(Chart, id=args.chart_id, country=args.country)

    log.debug("Chart found: {0} it has the following entries".format(chart.name))

    csvout = csv.writer(sys.stdout, delimiter='\t')

    if not args.no_header:
        csvout.writerow(["rank", "value", "artist_id", "artist_name", "releasegroup_id", "releasegroup_name"])

    for chartitem in chart:
        csvout.writerow([chartitem.rank,
                         chartitem.value,
                         chartitem._releasegroup.artist.id,
                         chartitem._releasegroup.artist.name,
                         chartitem._releasegroup.id,
                         chartitem._releasegroup.name])
