
import os
import sys
import logging

from pathlib import Path

from logging.handlers import RotatingFileHandler

from .temp import temp_dir

try:
    env_log_level = os.environ.get("DEVPY_LOG_LEVEL", -1)
    DEFAULT_LOG_LEVEL = int(env_log_level)
except ValueError:
    DEFAULT_LOG_LEVEL = getattr(logging, str(env_log_level).upper(), -1)

# todo: add pretty print
def autolog(
    level=DEFAULT_LOG_LEVEL,
    name=None,
    path=None,
    log_on_crash=True,
    log_filename=True,
    _cache={}
):

    if not name:
        try:
            name = Path(sys.argv[0]).with_suffix('').name
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

    steam_handler = logging.StreamHandler()
    logger.addHandler(steam_handler)

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
