from argparse import Namespace

import psutil
from prometheus_client import Gauge

USAGE_GAUGE = Gauge(
  "host_disk_usage",
  "Disk usage in %",
  labelnames=["hostname", "disk"]
)

def export(args: Namespace):
  disks = psutil.disk_partitions()

  for disk in disks:
    used = psutil.disk_usage(disk.mountpoint)
    USAGE_GAUGE.labels(args.hostname,disk.mountpoint).set(used.percent)
