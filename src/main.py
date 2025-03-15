import time
import socket
import logging
from argparse import ArgumentParser

import prometheus_client
from prometheus_client import start_http_server

import cpu
import mem
import disk

parser = ArgumentParser()

parser.add_argument(
  "-p","--port",
  help="Port to export on. Default 8080",
  default=8080,
  type=int
)

parser.add_argument(
  "-i","--interval",
  help="How often to update values",
  default=5,
  type=int
)

parser.add_argument(
  "--hostname",
  help=f"Hostname to add to metric label. Default \"{socket.gethostname()}\"",
  default=socket.gethostname()
)

args = parser.parse_args();

if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)

  logging.info("Start export on port %i", args.port)
  start_http_server(args.port)

  while True:
    time.sleep(args.interval)
    cpu.export(args)
    mem.export(args)
    disk.export(args)
