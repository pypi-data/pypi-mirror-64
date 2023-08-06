# -*- coding: utf-8 -*-
#
# Copyright 2020 ITRS Group Ltd. All rights reserved.
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from enum import Enum


class SeverityBase(object):

    def __init__(self, description):
        self.id = id
        self.description = description

    def get_id(self):
        return self.id

    def get_description(self):
        return self.description


class Severity(SeverityBase, Enum):
    NONE = 'NONE',
    CRITICAL = 'CRITICAL',
    ERROR = 'ERROR',
    WARN = 'WARN',
    INFO = 'INFO',
    DEBUG = 'DEBUG',
    TRACE = 'TRACE'
