#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2020  David Arroyo Menéndez

# Author: David Arroyo Menéndez <davidam@gnu.org>
# Maintainer: David Arroyo Menéndez <davidam@gnu.org>

# This file is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.

# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with damegender; see the file LICENSE.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301 USA,

import csv
import json

pathcsvfile = "files/names/names_ie/vsa10_1~2p.csv"
outmalescsvfile = "files/names/names_ie/names_ie_males.csv"
outfemalescsvfile = "files/names/names_ie/names_ie_females.csv"
outjsonfile = "files/names/names_ie/names_ie.json"


# JSON vsa10_1~2p.csv

d = {}
#string = '['
string = ""

with open(pathcsvfile) as csvfile:
    sexreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    next(sexreader, None)
    for row in sexreader:
        count = row[0]
        name = row[1]
        d[name] = {}

with open(pathcsvfile) as csvfile2:
    sexreader2 = csv.reader(csvfile2, delimiter=',', quotechar='"')
    next(sexreader2, None)
    for row in sexreader2:
        count = row[0]
        name = row[1]
        year = row[2]
        if (count != '".."'):
            d[name][year] = count



# l = d.values()

# print(l)
# for i in l:
#     count = 0
#     for j in range(1998, 2019):
#         print(count)

string = json.dumps(d)
print(string)
fo = open(outjsonfile, "w")
fo.write(string)
fo.close()


#for i in l:
