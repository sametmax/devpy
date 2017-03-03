
import os
import sys
import logging

from pathlib import Path

import colorlog

from logging.handlers import RotatingFileHandler

from .temp import temp_dir

try:
    env_log_level = os.environ.get("DEVPY_LOG_LEVEL", -1)
    DEFAULT_LOG_LEVEL = int(env_log_level)
except ValueError:
    DEFAULT_LOG_LEVEL = getattr(logging, str(env_log_level).upper(), -1)

env_color_log = str(os.environ.get("DEVPY_COLOR_LOG", True)).strip().lower()
DEFAULT_COLOR_LOG = env_color_log in ('true', 'yes', '1')


# todo: add pretty print
def autolog(
    level=DEFAULT_LOG_LEVEL,
    name=None,
    path=None,
    log_on_crash=True,
    log_filename=True,
    color_log=DEFAULT_COLOR_LOG,
    _cache={}
):

    if not name:
        try:
            name = Path(sys.argv[0]).absolute().with_suffix('').name
        except IndexError:
            pass

    if name in _cache:
        return _cache[name]

    logger = logging.getLogger(name)

    filelogger = logging.getLogger('__fileonly__')

    logger.setLevel(level)

    log_file = path or Path(temp_dir(name)) / "auto.log"

    formatter = logging.Formatter(
        '%(asctime)s :: %(levelname)s :: %(pathname)s :: %(message)s'
    )
    file_handler = RotatingFileHandler(log_file, 'a', 1000000, 1)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    filelogger.addHandler(file_handler)

    if color_log:
        stream_handler = colorlog.StreamHandler()
        colored_formatter = colorlog.ColoredFormatter(
            '%(log_color)s%(message)s',
            log_colors={
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white'
            }
        )
        stream_handler.setFormatter(colored_formatter)
    else:
        stream_handler = logging.StreamHandler()
    logger.addHandler(stream_handler)

    previous_hook = sys.excepthook

    def on_crash(type, value, tb):
        filelogger.critical(
            "The program crashed on:",
            exc_info=(type, value, tb)
        )
        previous_hook(type, value, tb)

    if log_on_crash:
        sys.excepthook = on_crash

    if log_filename:
        logger.info('Starting to log in "{}"'.format(log_file))

    _cache[name] = logger

    return logger
