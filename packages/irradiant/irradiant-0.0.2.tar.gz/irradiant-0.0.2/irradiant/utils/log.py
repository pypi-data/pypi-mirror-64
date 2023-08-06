import logging
import sys
import os
from colorama import init, Fore, Back, Style
init()


loggers = set()


def create_file_logger(name, path):
    log = logging.getLogger(name)
    if name not in loggers:
        log.propagate = False

        handler = logging.FileHandler(path)
        log.addHandler(handler)
        loggers.add(name)

    return log


def create_logger(name, color, full_line_color=False):
    log = logging.getLogger(name)
    if name not in loggers:
        log.propagate = False
        log.color = color

        handler = logging.StreamHandler(stream=sys.stdout)
        fmt = "[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] " + ("" if full_line_color else Style.RESET_ALL) + "%(message)s"
        handler.setFormatter(logging.Formatter(fmt=Style.BRIGHT + color + fmt + Style.RESET_ALL))
        log.addHandler(handler)
        loggers.add(name)

    return log


def disable_mpl_logging():
    for l in ('matplotlib', 'matplotlib.font_manager'):
        mpl_logger = logging.getLogger(l)
        mpl_logger.setLevel(logging.WARNING)


def format_packet(pkt):
    return pkt.summary()


LOGLEVEL = os.environ.get("LOGLEVEL", "INFO").upper()
logging.basicConfig(stream=sys.stdout, level=LOGLEVEL)
logger = logging.getLogger("default")
loggers.add("default")
