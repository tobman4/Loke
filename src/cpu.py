from argparse import Namespace
import logging

import psutil
from prometheus_client import Gauge

USAGE_GAUGE = Gauge(
  "host_cpu_usage",
  "CPU usage in %",
  labelnames=["host"]
)

UPTIME_GAUGE = Gauge(
    "host_uptime",
    "Host uptime in seconds",
    labelnames=["host"]
)

LOGGER = logging.getLogger("cpu")

def export(args: Namespace):
  try:
    usage = psutil.cpu_percent(interval=1)
    USAGE_GAUGE.labels(args.hostname).set(usage)

    boot_time_timestamp = psutil.boot_time()
    current_time_timestamp = time.time()
    uptime_seconds = current_time_timestamp - boot_time_timestamp
    UPTIME_GAUGE.labels(args.hostname).set(uptime_seconds)
  except Exception:
    LOGGER.exception("Failed to export CPU metrics")
