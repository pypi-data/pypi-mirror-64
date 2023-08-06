# -*- coding: utf-8 -*-
#
# Copyright 2019 ITRS Group Ltd. All rights reserved.
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from enum import Enum


class UnitBase(object):

    def __init__(self, description):
        self.id = id
        self.description = description

    def get_id(self):
        return self.id

    def get_description(self):
        return self.description


class Unit(UnitBase, Enum):
    Bytes = 'bytes',
    Kilobytes = 'kilobytes',
    Kibibytes = 'kibibytes',
    Megabits = 'megabits',
    Megabytes = 'megabytes',
    Mebibytes = 'mebibytes',
    Gigabytes = 'gigabytes',
    Gibibytes = 'gibibytes',
    Terabytes = 'terabytes',
    Tebibytes = 'tebibytes',
    Petabytes = 'petabytes',
    Pebibytes = 'pebibytes',
    Exabytes = 'exabytes',
    Exbibytes = 'exbibytes',
    BitsPerSecond = 'bits per second',
    BytesPerSecond = 'bytes per second',
    KibibytesPerSecond = 'kibibytes per second',
    MegabitsPerSecond = 'megabits per second',
    GigabitsPerSecond = 'gigabits per second',
    PerSecond = 'per second',
    Nanoseconds = 'nanoseconds',
    Microseconds = 'microseconds',
    Milliseconds = 'milliseconds',
    Seconds = 'seconds',
    Minutes = 'minutes',
    Hours = 'hours',
    Days = 'days',
    DegreesCelsius = 'degrees Celsius',
    Hertz = 'hertz',
    Megahertz = 'megahertz',
    Gigahertz = 'gigahertz',
    Percent = 'percent',
    Fraction = 'fraction',
    Cores = 'cores',
    Millicores = 'millicores',
    Microcores = 'microcores',
    Nanocores = 'nanocores'
