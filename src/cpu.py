from argparse import Namespace
import logging

import psutil
from prometheus_client import Gauge

USAGE_GAUGE = Gauge(
  "host_cpu_usage",
  "CPU usage in %",
  labelnames=["host"]
)

LOGGER = logging.getLogger("cpu")

def export(args: Namespace):
  try:
    usage = psutil.cpu_percent(interval=1)
    USAGE_GAUGE.labels(args.hostname).set(usage)
  except Exception:
    LOGGER.exception("Failed to export CPU metrics")
