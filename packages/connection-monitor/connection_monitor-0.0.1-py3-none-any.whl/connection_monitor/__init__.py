# coding: utf-8
"""This package provide :py:func:`monitor` to build network stats.

There's also a command-line utility, installed with the package, named
``monitor``.

"""

# ---- build-in imports ---------------------------------------------------
from __future__ import annotations

import csv
import dataclasses
import datetime
import logging
import pkgutil
import time
import typing
from pathlib import Path

# ---- third-party imports ------------------------------------------------
import click
import psutil
import requests


# ---- package metadata ---------------------------------------------------
#: filename providing the package version
VERSION_FN = 'VERSION'
try:
    # pkgutil.get_data output is a byte stream, that needs decoding
    RAW_VERSION = pkgutil.get_data(__name__, VERSION_FN)
except FileNotFoundError:
    logging.error("Cannot retrieve version: %s", exc_info=True)
    RAW_VERSION = None

if RAW_VERSION is None:
    #: version of the package
    __version__ = '0.0.0'
    __version_short__ = '0.0'  #: version of the package, short way
else:
    __version__ = RAW_VERSION.decode()
    # sanitize string by removing blank characters
    for char in ' \r\n\t':
        __version__ = __version__.replace(char, '')
    # short version: only the two first components
    __version_short__ = '.'.join(__version__.split('.')[:2])

# ---- constants definition -----------------------------------------------
#: verbosity levels
VERBOSITY = {0: logging.WARNING, 1: logging.INFO, 2: logging.DEBUG}
#: time between two requests (seconds)
DEFAULT_DELAY: float = 5.0
#: default host for latency checking
DEFAULT_HOST: str = 'http://siinergy.net'
#: default timeout for latency measurement (seconds)
DEFAULT_TIMEOUT: float = 5
#: default filename for writing the stats
DEFAULT_OUT_FFN: str = 'network_data.csv'
#: default path for writing the stats
DEFAULT_OUT_PATH: Path = Path(DEFAULT_OUT_FFN)
#: default CSV parameters
CSV_PARAMS = dict(delimiter=';', lineterminator='\n')


# ---- classes definition -------------------------------------------------
@dataclasses.dataclass
class NetworkStats:
    """Class to handle the network statistics.

    Addition and substraction are supported; latency is however neither
    added (righthand latency is kept) nor substracted (lefthand latency is
    kept).

    >>> ns0 = NetworkStats(in_bytes=2.2, out_bytes=3.2, latency_ms=10.2)
    >>> ns1 = NetworkStats(in_bytes=2.3, out_bytes=4.3, latency_ms=32.1)
    >>> ns1 + ns0
    NetworkStats(in_bytes=4.5, out_bytes=7.5, latency_ms=10.2)
    >>> diff = ns1 - ns0; (diff.in_bytes <= 0.1, diff.latency_ms == 32.1)
    (True, True)

    """

    in_bytes: float = 0.0  # bytes
    out_bytes: float = 0.0  # bytes
    latency_ms: float = 0.0  # milliseconds

    def __add__(self, other):
        return NetworkStats(in_bytes=self.in_bytes + other.in_bytes,
                            out_bytes=self.out_bytes + other.out_bytes,
                            latency_ms=other.latency_ms)

    def __sub__(self, other):
        return NetworkStats(in_bytes=self.in_bytes - other.in_bytes,
                            out_bytes=self.out_bytes - other.out_bytes,
                            latency_ms=self.latency_ms)


# ---- functions definition -----------------------------------------------
def monitor(
        out_path: Path = DEFAULT_OUT_PATH,
        host: str = DEFAULT_HOST,
        delay: float = DEFAULT_DELAY,
        csv_params: dict = None,
        ) -> None:
    """Monitor the network and write the stats to *out_ffn* in csv format.

    Args:
        out_path: where to write the measurements.
        host: address to connect for latency measurement.
        delay: time between two measurements.
        csv_params: definition of csv structure.

    """
    csv_params = csv_params or CSV_PARAMS
    with out_path.open('a') as fh_out:
        csv_out = csv.writer(fh_out, **csv_params)
        if fh_out.tell() == 0:  # write header only at file creation
            csv_out.writerow(['timestamp', 'bytes_in', 'bytes_out',
                              'latency(ms)'])
        # TODO: the stats shall be gathered from a queue
        for stats in get_stats_in_period(host=host):
            stats_strs: typing.List[str] = [
                str(datetime.datetime.now()),
                "{:.3f}".format(convert_to_mbit(stats.in_bytes)),
                "{:.3f}".format(convert_to_mbit(stats.out_bytes)),
                "{:.1f}".format(stats.latency_ms)]
            logging.info("%s: in: %sMB, out: %sMB, ping: %sms", *stats_strs)
            csv_out.writerow(stats_strs)
            # TODO: the *delay* should by in `get_stats_...` function
            time.sleep(delay)
            fh_out.flush()


def get_stats_in_period(
        host: str = DEFAULT_HOST,
        ) -> typing.Iterator[NetworkStats]:
    """Yield stats for the period between two calls.

    Args:
        host: address to connect to for latency measurement.

    Yields:
        latest i/o bytes counts and latency measurement.

    """
    old_stats = NetworkStats()
    while True:
        # TODO: this shall be done in a separate thread, as `latency() call`
        # is very likely to take some *seconds* when things go rough. Return
        # value shall be pushed in a queue with the request start timestamp
        new_stats = NetworkStats(
            in_bytes=psutil.net_io_counters().bytes_recv,
            out_bytes=psutil.net_io_counters().bytes_sent,
            latency_ms=latency(host=host),
            )
        if old_stats.in_bytes:
            yield new_stats - old_stats
        old_stats = new_stats


def latency(
        host: str = DEFAULT_HOST,
        timeout: float = DEFAULT_TIMEOUT,
        ) -> float:
    """Ping *host* and return the latency value in ms."""
    # TODO: do requests to different servers, to rotate somehow
    try:
        duration_ms = 1000.0 * \
            requests.head(host, timeout=timeout).elapsed.total_seconds()
    except (requests.ConnectionError, requests.exceptions.ReadTimeout):
        duration_ms = -1.0
    return duration_ms


def convert_to_mbit(value: float) -> float:
    """Convert *value* from Bytes to mega-Bytes.

    >>> round(convert_to_mbit(1_000_000.0), 2)
    0.95

    """
    return value / (1024.0 ** 2)


@click.command()
@click.option('-o', '--out-ffn', default=DEFAULT_OUT_FFN,
              help=("Filename for writing measurments. This file is opened "
                    "in append mode, so previous data is kept."))
@click.option('-h', '--host', type=str, default=DEFAULT_HOST,
              help=("Host to connect to, to measure latency."))
@click.option('-d', '--delay', type=float, default=DEFAULT_DELAY,
              help=("Time (in seconds) between two measurments."))
@click.option('-v', '--verbose', count=True, default=0,
              help=("Increase verbosity; default is to display WARNING "
                    "messages and higher. Set once, displays also INFO "
                    "messages; repeated, displays also DEBUG messages."))
@click.version_option()
def cli(
        out_ffn: str,
        host: str,
        delay: float,
        verbose: int,
        ) -> None:
    """Starts the monitoring."""
    logging.basicConfig(level=VERBOSITY[verbose])
    monitor(out_path=Path(out_ffn), host=host, delay=delay)


if __name__ == '__main__':
    monitor()
