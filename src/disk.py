from argparse import Namespace
import logging

import psutil
from prometheus_client import Gauge

USAGE_GAUGE = Gauge(
  "host_disk_usage",
  "Disk usage in %",
  labelnames=["hostname", "disk"]
)

LOGGER = logging.getLogger("disk")

def export(args: Namespace):
  try:
    disks = psutil.disk_partitions()
  except Exception:
    LOGGER.exception("Failed to list disk partitions")
    return

  for disk in disks:
    try:
      used = psutil.disk_usage(disk.mountpoint)
      USAGE_GAUGE.labels(args.hostname, disk.mountpoint).set(used.percent)
    except Exception:
      LOGGER.exception("Failed to export disk metrics for %s", disk.mountpoint)
