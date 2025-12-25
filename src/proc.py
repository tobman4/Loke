
from argparse import Namespace
from prometheus_client import Gauge
import psutil


NUM_PROC = Gauge(
    "host_proc_count",
    "Numpr of processes on host",
    labelnames=["host"]
)

def expor(args: Namespace):
    procs = psutil.pids()

    NUM_PROC.labels(args.hostname).set(len(procs))
