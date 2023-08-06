# -*- coding: utf-8 -*-
#
# Copyright 2019 ITRS Group Ltd. All rights reserved.
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

"""
ITRS statsd client library.

itrsstatsd is a Python library for sending metrics to an ITRS statsd server.

The module requires Python version 3.7 or greater.

Step 0 - In order to use this library it is necessary to first understand the
data model at a high level.

The following metric types are supported:
- Gauge (can be set or adjusted)
- Counter (can be incremented or decremented)
- Timer (can be set)
- Set (used to record unique IDs)
- Event (used to report events)
- Attribute (used to report static values)

The types are handled differently by the server so it is important to choose
the correct one.

Metrics of all types have common attributes:
- Name
- Value

Optionally, all metrics mey be decorated by dimensional labels
(i.e. key='value') pairs. These are used by the backend to differentiate
between metrics emitting entities. It is common for all metrics emitted by a
given application to all have the same dimensional labels so that they can be
associated with that application.

A unit of measure may also be associated with metrics, although this mainly
applies to Gauges.

Counters and Timers tend to be sent at high rates. It is possible to reduce
this by not sending all samples, i.e. by reducing the sample rate.

Events contain a message and an optional severity level, much like a log
message from an application.

Attributes  

Step 1a - Build a statsd client for a server running on either
os.environ['STATSD_SERVER'] or 'localhost' (if no env variable set) listening on
the port os.environ['STATSD_PORT'] or '8125' (if no env variable set):

    >>> from itrsstatsd import build_statsd
    >>> statsd = build_statsd()

Step 1b - Build a statsd client for a server running on
os.environ['STATSD_SERVER'] or 'localhost' (if no env variable set) listening on
a non-default port:

    >>> statsd = build_statsd(9876)

Step 1c - Build a statsd client for a server running on 'hostname' listening on
port os.environ['STATSD_PORT'] or '8125' (if no env variable set):

    >>> statsd = build_statsd('hostname')

Step 1d - Build a statsd client for a server running on 'hostname' listening on
a non-default port:

    >>> statsd = build_statsd('hostname', 9876)

Step 1e - Build a statsd client that uses TCP instead of the default UDP:

    >>> statsd = build_statsd(protocol='tcp')

It is also possible to build a test statsd client which prints to stdout
instead of sending to a server:

    >>> statsd = build_test_statsd()

Step 2 - Set default dimensions (optional, but recommended):

    >>> statsd.default_dimension('dimension', 'value')
    >>> statsd.default_dimensions(dimension1='some_value', dimension2='another_value')

The following environment variables may be used to set default dimensions (designed for
orchestrated environments like Kubernetes or OpenShift):
- NAMESPACE
- CONTAINER_NAME
- POD_NAME
- HOSTNAME

If a Kuberentes/OpenShift environment is not detected, the client will fall back on these environment
variables instead:
- HOSTNAME
- APP_NAME

Step 3 - Send metrics.  Note that these methods never block and any OSErrors will be caught and printed to stderr.

    >>> statsd.gauge("gauge_name_1", 1234567)

    >>> from itrsstatsd import Unit as Unit
    >>> statsd.gauge("gauge_name_2", 67.5, Unit.Percent)
    >>> statsd.gauge("gauge_name_3", 9876544321, Unit.Bytes)
    >>> statsd.adjust_gauge("gauge_name_3", -22345, Unit.Bytes)

    >>> statsd.increment("counter_name_1")
    >>> statsd.decrement("counter_name_1")
    >>> statsd.count("counter_name_1", 25)

    >>> statsd.timer("timer_name_1", 245)
    >>> statsd.timer("timer_name_2", 324.524)
    >>> statsd.timer("timer_name_3", 256.357954)

    >>> statsd.unique("set_name_1", "ID1")
    >>> statsd.unique("set_name_1", "ID2")
    >>> statsd.unique("set_name_1", "ID3")

    >>> statsd.event("event_name_1", "event_message", Severity.INFO)
    >>> statsd.event("event_name_2", "event_message", Severity.DEBUG)
    >>> statsd.event("event_name_3", "event_message", Severity.CRITICAL)

    >>> statsd.attribute("attr_name_1", "A1")
    >>> statsd.attribute("attr_name_2", "A2")
    >>> statsd.attribute("attr_name_3", "A3")

Metrics can also be sent with additional dimensions:

    >>> statsd.increment("counter_name_2", dim1='value', dim2='some_other_value')
    >>> statsd.gauge("gauge_name_4", 67.5, Unit.Percent, dim1='value', dim2='some_other_value')
    >>> statsd.timer("timer_name_4", 124, dim1='value', dim2='some_other_value')
    >>> statsd.unique("set_name_1", "ID4", dim1='value', dim2='some_other_value')
    >>> statsd.event("event_name_3", "event_message", Severity.CRITICAL, dim1='value', dim2='some_other_value')
    >>> statsd.attribute("attr_name_1", "A1", dim1='value', dim2='some_other_value')
        
For Counters and Timers it is possible to specify the sample rate, which
governs the probability of the the metric being sent to the statsd server.
In the examples below metrics are only sent to the server approximately 50%
of the time:

    >>> statsd.increment("counter_name_1", 0.5)
    >>> statsd.timer("timer_name_1", 245, 0.5)
"""

from .__version__ import __version__, __description__, __url__, __copyright__, __author__, __author_email__
from .api import Api
from .units import Unit
from .severity import Severity
from .statsd import build_statsd, build_test_statsd
import sys

if sys.version_info[0] != 3 or sys.version_info[1] < 7:
    print("This package requires at least Python version 3.7")
    sys.exit(1)

