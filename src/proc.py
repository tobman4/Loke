
from argparse import Namespace
import logging

from prometheus_client import Gauge
import psutil


NUM_PROC = Gauge(
    "host_proc_count",
    "Numpr of processes on host",
    labelnames=["host"]
)

PROC_CPU_GAUGE = Gauge(
    "host_proc_cpu_percent",
    "CPU percent used by the top processes",
    labelnames=["host", "pid", "name"]
)

LOGGER = logging.getLogger("proc")

def export(args: Namespace):
    try:
        procs = list(psutil.process_iter(["pid", "name"]))

        for proc in procs:
            try:
                proc.cpu_percent(interval=None)
            except Exception:
                LOGGER.debug("Failed to read CPU percent for pid %s", proc.info.get("pid"))

        top_procs = sorted(
            procs,
            key=lambda proc: proc.cpu_percent(interval=None),
            reverse=True
        )[:10]

        NUM_PROC.labels(args.hostname).set(len(procs))
        PROC_CPU_GAUGE.clear()
        for proc in top_procs:
            PROC_CPU_GAUGE.labels(
                args.hostname,
                str(proc.info.get("pid")),
                proc.info.get("name") or "unknown"
            ).set(proc.cpu_percent(interval=None))
    except Exception:
        LOGGER.exception("Failed to export process metrics")
