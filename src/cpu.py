import psutil
from prometheus_client import Gauge

USAGE_GAUGE = Gauge(
  "host_cpu_usage",
  "CPU usage in %"
)

def export():
  usage = psutil.cpu_percent(interval=1)
  USAGE_GAUGE.set(usage)
