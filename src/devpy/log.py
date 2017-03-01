
import sys
import logging
import inspect

from pathlib import Path

from logging.handlers import RotatingFileHandler

from .temp import temp_dir


# todo: add pretty print
def autolog(name=None, path=None, log_on_crash=True, _cache={}):

    if not name:
        try:
            name = Path(sys.argv[0]).name
        except IndexError:
            pass
    if not name:
        outer_frame = inspect.getouterframes(inspect.currentframe())[1].frame
        name = outer_frame.f_globals.get('__name__', 'any_devpy').split('.')[0]

    if name in _cache:
        return _cache[name]

    log_file = path or Path(temp_dir(name)) / "auto.log"

    logger = logging.getLogger(name)

    formatter = logging.Formatter(
        '%(asctime)s :: %(levelname)s :: %(pathname)s :: %(message)s'
    )

    file_handler = RotatingFileHandler(log_file, 'a', 1000000, 1)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    steam_handler = logging.StreamHandler()
    steam_handler.setLevel(logging.DEBUG)
    logger.addHandler(steam_handler)

    previous_hook = sys.excepthook

    def on_crash(type, value, tb):
        logging.exception(f"The program crashed on: {value}")
        previous_hook(type, value, tb)

    if log_on_crash:
        sys.excepthook = on_crash

    logger.info(f'Starting to log in "{log_file}"')

    _cache[name] = logger

    return logger
