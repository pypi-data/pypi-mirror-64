# -*- coding: utf-8 -*-
#
# Copyright 2019 ITRS Group Ltd. All rights reserved.
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from .units import Unit
from .severity import Severity


class Api:

    def __init__(self, sender):
        """Construct an API object.

        :param sender: The metrics sender object.
        """

        self.sender = sender
        self.dimensions = {}
        self.closed = False

    def close(self):
        """Close the API and underlying resources."""

        self.sender.close()
        self.dimensions.clear()
        self.closed = True

    def default_dimension(self, key, value):
        """Add a default dimension to be included with all metrics.

        :param key: Dimension key.
        :param value: Dimension value.
        """

        self.dimensions[key] = value

    def default_dimensions(self, **dimension_kwargs):
        """Set the default dimensions to be included with all metrics.

        :param dimension_kwargs: Dimension key='value' pairs.
        """

        self.dimensions.update(dimension_kwargs)

    def increment(self, name, sample_rate: float = 1.0, **dimension_kwargs):
        """Increment the named counter by 1.

        :param name: The counter name.
        :param sample_rate: (optional, default is 1.0) If 0.0 < sample_rate < 1.0 then samples are only sent to the
            server for sample_rate * 100 percent of invocations.
        :param dimension_kwargs: (optional) Additional dimension key='value' pairs to send to the server.
        """

        self.count(name, 1, sample_rate, **dimension_kwargs)

    def decrement(self, name, sample_rate: float = 1.0, **dimension_kwargs):
        """Decrement the named counter by 1.

        :param name: The counter name.
        :param sample_rate: (optional, default is 1.0) If 0.0 < sample_rate < 1.0 then samples are only sent to the
            server for sample_rate * 100 percent of invocations.
        :param dimension_kwargs: (optional) Additional dimension key='value' pairs to send to the server.
        """

        self.count(name, -1, sample_rate, **dimension_kwargs)

    def count(self, name, delta, sample_rate: float = 1.0, **dimension_kwargs):
        """Adjust the named counter by the specified delta.

        :param name: The counter name.
        :param delta The count delta.
        :param sample_rate: (optional, default is 1.0) If 0.0 < sample_rate < 1.0 then samples are only sent to the
            server for sample_rate * 100 percent of invocations.
        :param dimension_kwargs: (optional) Additional dimension key='value' pairs to send to the server.
        """

        if not self.closed:
            self.sender.on_counter(name, delta, sample_rate, **merge(self.dimensions, **dimension_kwargs))

    def gauge(self, name, value: float, unit: Unit = None, **dimension_kwargs):
        """Set the named gauge to the specified value.

        :param name: The gauge name.
        :param value The gauge value.
        :param unit: (optional, default is None) The unit to associate with the named gauge.
        :param dimension_kwargs: (optional) Additional dimension key='value' pairs to send to the server.
        """

        if not self.closed:
            self.sender.on_gauge(name, value, False, unit, **merge(self.dimensions, **dimension_kwargs))

    def adjust_gauge(self, name, delta: float, unit: Unit = None, **dimension_kwargs):
        """Adjust the named gauge by the specified delta.

        :param name: The gauge name.
        :param delta The gauge value delta.
        :param unit: (optional, default is None) The unit to associate with the named gauge.
        :param dimension_kwargs: (optional) Additional dimension key='value' pairs to send to the server.
        """

        if not self.closed:
            self.sender.on_gauge(name, delta, True, unit, **merge(self.dimensions, **dimension_kwargs))

    def unique(self, name, identifier, **dimension_kwargs):
        """Report a unique value in a bucket or "set".

        The server will track the number of unique identifiers in the named set and report as a counter.

        :param name: The set name.
        :param identifier The set identifier.
        :param dimension_kwargs: (optional) Additional dimension key='value' pairs to send to the server.
        """

        if not self.closed:
            self.sender.on_set(name, identifier, **merge(self.dimensions, **dimension_kwargs))

    def timer(self, name, elapsed, sample_rate: float = 1.0, **dimension_kwargs):
        """Report elapsed milliseconds of a timed operation.

        :param name: The operation name.
        :param elapsed The elapsed time in milliseconds.  The value can be an integer or a floating point value
            whose decimal value represents microseconds or nanoseconds.
        :param sample_rate: (optional, default is 1.0) If 0.0 < sample_rate < 1.0 then samples are only sent to the
            server for sample_rate * 100 percent of invocations.
        :param dimension_kwargs: (optional) Additional dimension key='value' pairs to send to the server.
        """

        if not self.closed:
            self.sender.on_timer(name, elapsed, sample_rate, **merge(self.dimensions, **dimension_kwargs))

    def event(self, name, message, severity: Severity = Severity.NONE, **dimension_kwargs):
        """Report a named event with a message and severity level.

        :param name: The operation name.
        :param message The event message.
        :param severity: (optional, default is NONE)
        :param dimension_kwargs: (optional) Additional dimension key='value' pairs to send to the server.
        """

        if not self.closed:
            self.sender.on_event(name, message, severity, **merge(self.dimensions, **dimension_kwargs))

    def attribute(self, name, value, **dimension_kwargs):
        """Report a named static attribute.

        :param name: The operation name.
        :param value The attribute value
        :param dimension_kwargs: (optional) Additional dimension key='value' pairs to send to the server.
        """

        if not self.closed:
            self.sender.on_attribute(name, value, **merge(self.dimensions, **dimension_kwargs))


def merge(dimensions, **dimension_kwargs):
    merged_dimensions = dimensions.copy()
    merged_dimensions.update(dimension_kwargs)
    return merged_dimensions
