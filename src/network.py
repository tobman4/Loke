from argparse import Namespace
import logging
import time

import psutil
from prometheus_client import Gauge

BYTES_SENT_GAUGE = Gauge(
  "host_net_bytes_sent_per_sec",
  "Bytes sent per second per interface",
  labelnames=["host", "interface"]
)

BYTES_RECV_GAUGE = Gauge(
  "host_net_bytes_recv_per_sec",
  "Bytes received per second per interface",
  labelnames=["host", "interface"]
)

LOGGER = logging.getLogger("network")

_LAST_STATS = {}
_LAST_TIMESTAMP = None

def export(args: Namespace):
  global _LAST_TIMESTAMP

  try:
    counters = psutil.net_io_counters(pernic=True)
  except Exception:
    LOGGER.exception("Failed to list network interfaces")
    return

  now = time.monotonic()
  previous_timestamp = _LAST_TIMESTAMP
  _LAST_TIMESTAMP = now

  if previous_timestamp is None:
    _LAST_STATS.clear()
    for interface, stats in counters.items():
      _LAST_STATS[interface] = (stats.bytes_sent, stats.bytes_recv)
    return

  elapsed = now - previous_timestamp
  if elapsed <= 0:
    return

  for interface, stats in counters.items():
    try:
      previous = _LAST_STATS.get(interface)
      if previous is None:
        _LAST_STATS[interface] = (stats.bytes_sent, stats.bytes_recv)
        continue

      prev_sent, prev_recv = previous
      sent_per_sec = (stats.bytes_sent - prev_sent) / elapsed
      recv_per_sec = (stats.bytes_recv - prev_recv) / elapsed
      BYTES_SENT_GAUGE.labels(args.hostname, interface).set(sent_per_sec)
      BYTES_RECV_GAUGE.labels(args.hostname, interface).set(recv_per_sec)
      _LAST_STATS[interface] = (stats.bytes_sent, stats.bytes_recv)
    except Exception:
      LOGGER.exception("Failed to export network metrics for %s", interface)
