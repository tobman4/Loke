import time
import logging
from argparse import ArgumentParser

import prometheus_client
from prometheus_client import start_http_server

import cpu
import mem

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

args = parser.parse_args();

if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)

  logging.info("Start export on port %i", args.port)
  start_http_server(args.port)

  while True:
    time.sleep(args.interval)
    cpu.export()
    mem.export()
