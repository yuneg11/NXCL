import os
import random
import logging

from datetime import datetime
from typing import Optional, Iterable


def get_experiment_name(random_code: str = None) -> str:
    now = datetime.now().strftime("%y%m%d-%H%M%S")
    if random_code is None:
        random_code = "".join(random.choices("abcdefghikmnopqrstuvwxyz", k=4))
    return  now + "-" + random_code


def link_output_dir(output_dir: str, subnames: Iterable[str]):
    link_dir = os.path.join("outs", *subnames, os.path.basename(output_dir))
    os.makedirs(os.path.dirname(link_dir), exist_ok=True)
    os.symlink(os.path.join(*([".."] * len(subnames)), "_", os.path.basename(output_dir)), link_dir)


def setup_logger(logger_name: str, output_dir: str, suppress: Iterable = ()):
    from nxcl.rich.logging import RichHandler, RichFileHandler

    LOG_SHORT_FORMAT = "[%(asctime)s] %(message)s"
    LOG_LONG_FORMAT = "[%(asctime)s][%(levelname)s] %(message)s"
    LOG_DATE_SHORT_FORMAT = "%H:%M:%S"
    LOG_DATE_LONG_FORMAT = "%Y-%m-%d %H:%M:%S"

    logger = logging.getLogger(logger_name)
    logger.propagate = False
    logger.setLevel(logging.DEBUG)

    stream_handler = RichHandler(tracebacks_suppress=suppress)
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(logging.Formatter(fmt=LOG_SHORT_FORMAT, datefmt=LOG_DATE_SHORT_FORMAT))
    logger.addHandler(stream_handler)

    debug_file_handler = RichFileHandler(os.path.join(output_dir, "debug.log"), mode="a")
    debug_file_handler.setLevel(logging.DEBUG)
    debug_file_handler.setFormatter(logging.Formatter(fmt=LOG_LONG_FORMAT, datefmt=LOG_DATE_LONG_FORMAT))
    logger.addHandler(debug_file_handler)

    info_file_handler = RichFileHandler(os.path.join(output_dir, "info.log"), mode="a", tracebacks_suppress=suppress)
    info_file_handler.setLevel(logging.INFO)
    info_file_handler.setFormatter(logging.Formatter(fmt=LOG_SHORT_FORMAT, datefmt=LOG_DATE_LONG_FORMAT))
    logger.addHandler(info_file_handler)

    return logger


class AverageMeter:
    def __init__(self, *names):
        self.names = names
        self.sums = {k: 0 for k in names}
        self.cnts = {k: 0 for k in names}

    def reset(self):
        self.sums = {k: 0 for k in self.names}
        self.cnts = {k: 0 for k in self.names}

    def update(self, values: Optional[dict] = None, n: int = 1, **kwargs):
        if values is None:
            values = kwargs
        else:
            values = {**values, **kwargs}

        for k, v in values.items():
            self.sums[k] += v * n
            self.cnts[k] += n

    @property
    def value(self):
        return {k: self.sums[k] / self.cnts[k] for k in self.names}

    def __getattr__(self, name):
        if name in self.names:
            return self.sums[name] / self.cnts[name]
        else:
            raise AttributeError(f"{name} is not recorded metric")

    def __getitem__(self, name):
        if name in self.names:
            return self.sums[name] / self.cnts[name]
        else:
            raise KeyError(f"{name} is not recorded metric")
