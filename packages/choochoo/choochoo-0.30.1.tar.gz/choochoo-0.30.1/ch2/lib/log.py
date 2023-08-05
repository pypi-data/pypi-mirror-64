
from logging import getLogger, DEBUG, Formatter, INFO, StreamHandler, WARNING
from logging.handlers import RotatingFileHandler
from os.path import join
from sys import exc_info
from traceback import format_tb

from ..commands.args import COMMAND, LOGS, PROGNAME, VERBOSITY, LOG, TUI

log = getLogger(__name__)


def make_log(args):

    if not getLogger('ch2').handlers:

        level = 10 * (6 - args[VERBOSITY])

        file_formatter = Formatter('%(levelname)-8s %(asctime)s: %(message)s')
        name = args[LOG] if LOG in args and args[LOG] else (
                (args[COMMAND] if COMMAND in args and args[COMMAND] else PROGNAME) + f'.{LOG}')
        path = join(args.dir(LOGS), name)
        file_handler = RotatingFileHandler(path, maxBytes=1e6, backupCount=10)
        file_handler.setLevel(DEBUG)
        file_handler.setFormatter(file_formatter)

        slog = getLogger('sqlalchemy')
        slog.setLevel(WARNING)
        slog.addHandler(file_handler)

        mlog = getLogger('matplotlib')
        mlog.setLevel(INFO)
        mlog.addHandler(file_handler)

        blog = getLogger('bokeh')
        blog.setLevel(DEBUG)
        blog.addHandler(file_handler)

        tlog = getLogger('tornado')
        tlog.setLevel(INFO)
        tlog.addHandler(file_handler)

        sslog = getLogger('sentinelsat')
        sslog.setLevel(DEBUG)
        sslog.addHandler(file_handler)

        wlog = getLogger('werkzeug')
        wlog.setLevel(DEBUG)
        wlog.addHandler(file_handler)

        clog = getLogger('ch2')
        clog.setLevel(DEBUG)
        clog.addHandler(file_handler)

        # capture logging from an executing module, if one exists
        xlog = getLogger('__main__')
        xlog.setLevel(DEBUG)
        xlog.addHandler(file_handler)

        if not args[TUI]:
            stderr_formatter = Formatter('%(levelname)8s: %(message)s')
            stderr_handler = StreamHandler()
            stderr_handler.setLevel(level)
            stderr_handler.setFormatter(stderr_formatter)
            blog.addHandler(stderr_handler)
            tlog.addHandler(stderr_handler)
            wlog.addHandler(stderr_handler)
            clog.addHandler(stderr_handler)
            xlog.addHandler(stderr_handler)


def log_current_exception(traceback=True):
    t, e, tb = exc_info()
    try:
        log.debug(f'Exception: {e}')
    except:
        pass
    log.debug(f'Type: {t}')
    if traceback:
        log.debug('Traceback:\n' + ''.join(format_tb(tb)))
