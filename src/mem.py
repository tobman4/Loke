from argparse import Namespace
import logging

import psutil

from prometheus_client import Gauge

PERCENT_GAUGE = Gauge(
  "host_mem_percent",
  "percent of memory in use",
  labelnames=["host"]
)

USED_GAUGE = Gauge(
  "host_mem_used",
  "Used memory now",
  labelnames=["host"]
)

LOGGER = logging.getLogger("mem")

def export(args: Namespace):
  try:
    mem = psutil.virtual_memory()
    USED_GAUGE.labels(args.hostname).set(mem.used)
    PERCENT_GAUGE.labels(args.hostname).set(mem.percent)
  except Exception:
    LOGGER.exception("Failed to export memory metrics")
