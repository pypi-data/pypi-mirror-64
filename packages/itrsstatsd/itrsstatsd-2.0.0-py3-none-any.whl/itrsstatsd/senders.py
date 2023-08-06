# -*- coding: utf-8 -*-
#
# Copyright 2019 ITRS Group Ltd. All rights reserved.
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import random
import sys
import threading
import time

from .units import Unit
from .severity import Severity


class StatsdMetricsSender:

    def __init__(self, channel, capacity=1024):
        self._channel = channel
        self._queue = CircularQueue(capacity=capacity)
        self._stop_event = threading.Event()
        self._drop_event = threading.Event()
        self._warned_drop = False
        self._connected = False
        self._last_connect = 0
        self._sender_thread = threading.Thread(target=self._process_queue, daemon=True).start()

    def close(self):
        self._stop_event.set()
        self._close_channel()

    def _close_channel(self):
        self._connected = False
        self._channel.close()

    def on_counter(self, name, count, sample_rate: float, **dimension_kwargs):
        if not _should_send(sample_rate):
            return

        counter = f"{name}:{count}|c"

        if 0.0 < sample_rate < 1.0:
            counter += f"|@{sample_rate}"

        self._enqueue(_append_dimensions(counter, **dimension_kwargs))

    def on_gauge(self, name, value: float, is_delta: bool, unit: Unit, **dimension_kwargs):
        gauge = f"{name}:"

        if is_delta and value > 0.0:
            gauge += "+"

        gauge += f"{value}|g"

        if unit is not None:
            gauge += f"|u:{unit.get_description()}"

        self._enqueue(_append_dimensions(gauge, **dimension_kwargs))

    def on_set(self, name, identifier, **dimension_kwargs):
        gauge = f"{name}:{identifier}|s"
        self._enqueue(_append_dimensions(gauge, **dimension_kwargs))

    def on_timer(self, name, elapsed, sample_rate: float, **dimension_kwargs):
        if not _should_send(sample_rate):
            return

        timer = f"{name}:{elapsed}|ms"

        if 0.0 < sample_rate < 1.0:
            timer += f"|@{sample_rate}"

        self._enqueue(_append_dimensions(timer, **dimension_kwargs))

    def on_event(self, name, message, severity: Severity, **dimension_kwargs):
        if message.find('\n') != -1:
            message = message.replace('\n', '\\n')
        message_bytes_len = str(len(message.encode("UTF-8")))
        timestamp_millis = str(int(round(time.time() * 1000)))
        severity_name = severity.get_description()

        event = f"{name}:{message_bytes_len}|e|{message}|t:{timestamp_millis}|s:{severity_name}"

        self._enqueue(_append_dimensions(event, **dimension_kwargs))

    def on_attribute(self, name, value, **dimension_kwargs):
        if value.find('\n') != -1:
            value = value.replace('\n', '\\n')
        value_bytes_len = str(len(value.encode("UTF-8")))

        attribute = f"{name}:{value_bytes_len}|a|{value}"

        self._enqueue(_append_dimensions(attribute, **dimension_kwargs))

    def _enqueue(self, msg):
        if self._queue.add(msg) > 0 and not self._warned_drop:
            self._warned_drop = True
            print("At least one statsd message was dropped due to a full sending queue. " +
                  "This may indicate a network problem or that a larger sending queue size " +
                  "is necessary to support the load. This error will not be logged again.",
                  file=sys.stderr)

    def _process_queue(self):
        while not self._stop_event.is_set():
            if self._connected or self._connect():
                msg = self._queue.poll(.1)
                if msg is not None:
                    try:
                        self._channel.send(msg)
                    except Exception as e:
                        print("Failed to send statsd message: {}".format(str(e)), file=sys.stderr)
                        self._close_channel()

    def _connect(self):
        now = time.time()
        if now - self._last_connect >= 10:
            self._last_connect = now
            try:
                self._channel.connect()
                self._connected = True
                return True
            except Exception as e:
                print("Failed to connect to statsd server: {0}".format(str(e)), file=sys.stderr)

        time.sleep(.1)
        self._connected = False
        return False


def _should_send(sample_rate: float):
    if sample_rate <= 0.0:
        return False

    if sample_rate >= 1.0:
        return True

    return sample_rate > random.random()


def _append_dimensions(message, **dimension_kwargs):
    if dimension_kwargs is not None and len(dimension_kwargs) > 0:
        message += "|#"
        for key, value in dimension_kwargs.items():
            message += f"{key}:{value},"
        message = message[0:-1]

    return message


class CircularQueue:

    def __init__(self, capacity=1024):
        self._elements = [None] * capacity
        self._start = 0
        self._end = 0
        self._capacity = capacity
        self._full = False
        self._lock = threading.RLock()
        self._not_empty = threading.Condition(self._lock)
        self._dropped = 0

    def add(self, msg):
        """Returns total number of messages dropped"""

        with self._lock:
            if self._full:
                self._increment_start()
                self._dropped += 1

            self._elements[self._end] = msg
            self._increment_end()

            if self._end == self._start:
                self._full = True

            self._not_empty.notify()
        return self._dropped

    def _increment_start(self):
        self._start += 1
        if self._start == self._capacity:
            self._start = 0

    def _increment_end(self):
        self._end += 1
        if self._end == self._capacity:
            self._end = 0

    def poll(self, timeout):
        msg = None
        with self._lock:
            if self._size() > 0 or self._not_empty.wait(timeout):
                msg = self._elements[self._start]
                self._elements[self._start] = None
                self._increment_start()
                self._full = False
        return msg

    def _size(self):
        if self._start == self._end:
            return self._capacity if self._full else 0
        if self._end < self._start:
            return self._capacity - self._start + self._end
        return self._end - self._start

    def size(self):
        with self._lock:
            return self._size()
