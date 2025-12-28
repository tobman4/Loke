from argparse import Namespace
import logging

import psutil
from prometheus_client import Gauge

BYTES_SENT_GAUGE = Gauge(
  "host_net_bytes_sent",
  "Bytes sent per interface",
  labelnames=["host", "interface"]
)

BYTES_RECV_GAUGE = Gauge(
  "host_net_bytes_recv",
  "Bytes received per interface",
  labelnames=["host", "interface"]
)

LOGGER = logging.getLogger("network")

def export(args: Namespace):
  try:
    counters = psutil.net_io_counters(pernic=True)
  except Exception:
    LOGGER.exception("Failed to list network interfaces")
    return

  for interface, stats in counters.items():
    try:
      BYTES_SENT_GAUGE.labels(args.hostname, interface).set(stats.bytes_sent)
      BYTES_RECV_GAUGE.labels(args.hostname, interface).set(stats.bytes_recv)
    except Exception:
      LOGGER.exception("Failed to export network metrics for %s", interface)
