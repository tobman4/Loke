from argparse import Namespace
import psutil
from prometheus_client import Gauge

USAGE_GAUGE = Gauge(
  "host_cpu_usage",
  "CPU usage in %",
  labelnames=["host"]
)

def export(args: Namespace):
  usage = psutil.cpu_percent(interval=1)
  USAGE_GAUGE.labels(args.hostname).set(usage)
