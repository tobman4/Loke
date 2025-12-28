import time
import socket
import logging
from argparse import ArgumentParser

import prometheus_client
from prometheus_client import start_http_server

import cpu
import mem
import disk
import proc

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

parser.add_argument(
    "-a", "--address",
    default="0.0.0.0"
)

args = parser.parse_args();

if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)

  logging.info("Start export on port %s:%i", args.address, args.port)
  start_http_server(args.port, addr=args.address)

  while True:
    time.sleep(args.interval)
    cpu.export(args)
    mem.export(args)
    disk.export(args)
    proc.export(args)
