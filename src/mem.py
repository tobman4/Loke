import psutil

from prometheus_client import Gauge

PERCENT_GAUGE = Gauge(
  "host_mem_percent",
  "percent of memory in use"
)

USED_GAUGE = Gauge(
  "host_mem_used",
  "Used memory now"
)

def export():
  mem = psutil.virtual_memory()
  USED_GAUGE.set(mem.used)
  PERCENT_GAUGE.set(mem.percent)
