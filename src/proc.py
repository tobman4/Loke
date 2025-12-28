
from argparse import Namespace
import logging

from prometheus_client import Gauge
import psutil


NUM_PROC = Gauge(
    "host_proc_count",
    "Numpr of processes on host",
    labelnames=["host"]
)

LOGGER = logging.getLogger("proc")

def expor(args: Namespace):
    try:
        procs = psutil.pids()

        NUM_PROC.labels(args.hostname).set(len(procs))
    except Exception:
        LOGGER.exception("Failed to export process metrics")
