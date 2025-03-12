from argparse import Namespace
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

def export(args: Namespace):
  mem = psutil.virtual_memory()
  USED_GAUGE.labels(args.hostname).set(mem.used)
  PERCENT_GAUGE.labels(args.hostname).set(mem.percent)
