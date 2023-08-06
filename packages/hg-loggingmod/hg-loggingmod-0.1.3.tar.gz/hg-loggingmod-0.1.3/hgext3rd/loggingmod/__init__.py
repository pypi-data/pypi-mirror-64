# Copyright 2019-2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License_indentifier: GPL-2.0-or-later
"""An extension to route all Mercurial UI output to the logging module."""
import json
import logging
from mercurial import (
    exthelper,
    demandimport,
)
from . import (
    sentry,
)
from .config import (
    CONFIG_SECTION,
    DEFAULT_GENERAL_FORMAT,
    DEFAULT_HG_FORMAT,
    loglevel,
)


hg_logger = logging.getLogger('hg')
# Formats used in hg_logger usually make use of the
# extra 'repo' parameter, that events emitted through other loggers
# don't have. We'll pair hg_logger with a specific handler, and block
# propagation.
hg_logger.propagate = False

eh = exthelper.exthelper()
uisetup = eh.finaluisetup


def cookextra(ui):
    # hgweb sets 'ui.forcecwd' on repo.ui to repo.root
    # ui.confisource() returns empty string if item not found
    if ui.configsource('ui', 'forcecwd') == 'hgweb':
        repodir = ui.config('ui', 'forcecwd')
    else:
        # suitable for command-line invocation (set in dispatch.py)
        repodir = ui.config('bundle', 'mainreporoot', default=None)
    return {'repo': repodir}


def error(self, *msg, **opts):
    hg_logger.error(''.join(msg).rstrip('\n'),
                    extra=cookextra(self))


def warn(self, *msg, **opts):
    hg_logger.warn(''.join(msg).rstrip('\n'),
                   extra=cookextra(self))


def debug(self, *msg, **opts):
    hg_logger.debug(''.join(msg).rstrip('\n'),
                    extra=cookextra(self))


def note(self, *msg, **opts):
    hg_logger.info(''.join(msg).rstrip('\n'),
                   extra=cookextra(self))


def log(self, event, msgfmt, *msgargs, **opts):
    logger = logging.getLogger('hg.' + event)
    level = logging.DEBUG if event == 'extension' else logging.INFO
    logger.log(level, msgfmt.rstrip('\n'), *msgargs,
               extra=cookextra(self))


_missing = object()


class MissingRepoFilter(logging.Filter):
    """A Filter to add repo=None to records that don't have repos.

    With formats using the 'repo' extra parameter, it leads to an error
    if that parameter is not explicitely passed while logging.

    This is cumbersome for direct callers of `hg_logger` that don't have
    repository information.
    """

    def filter(self, record):
        if getattr(record, 'repo', _missing) is _missing:
            record.repo = None
        return True


@eh.uisetup
def _uisetup(ui):
    logger = logging.getLogger(__name__)
    level = ui.configwith(loglevel, CONFIG_SECTION, 'level', default='INFO')
    fmt = ui.config(CONFIG_SECTION, 'format', default=DEFAULT_GENERAL_FORMAT)

    general_fmt = fmt.replace('%(repo)s', '')
    datefmt = "%Y-%m-%d %H:%M:%S %z"

    conf = dict(level=level,
                format=general_fmt,
                datefmt=datefmt)
    fpath = ui.config(CONFIG_SECTION, 'file', default=None)
    if fpath is not None:
        conf['filename'] = fpath
    logging.basicConfig(**conf)

    if general_fmt != fmt:
        logger.warning("Had to replace format %r by %r for non-Mercurial "
                       "logging because the 'repo' key can't be used outside "
                       "of the Mercurial context. "
                       "You may want to make separate configurations using "
                       "The 'format' and 'hg_format' settings.",
                       fmt, general_fmt)

    if fpath is None:
        hg_handler = logging.StreamHandler()
    else:
        hg_handler = logging.FileHandler(fpath)
    hg_handler.setFormatter(
        logging.Formatter(fmt=ui.config(CONFIG_SECTION, 'hg_format',
                                        default=DEFAULT_HG_FORMAT),
                          datefmt=datefmt)
    )
    hg_handler.addFilter(MissingRepoFilter())
    hg_logger.addHandler(hg_handler)

    jsonconf = ui.config(CONFIG_SECTION, 'config.json', default=None)
    logger.info("jsonconf=%r", jsonconf)
    if jsonconf is not None:
        with open(jsonconf) as conffile:
            conf_dict = json.load(conffile)
        logging.config.dictConfig(conf_dict)

    iniconf = ui.config(CONFIG_SECTION, 'config.ini', default=None)
    if iniconf is not None:
        logging.config.fileConfig(iniconf)

    if ui.config(CONFIG_SECTION, 'sentry.dsn', default=False):
        sentry.setup(ui)

    cls = ui.__class__
    cls.error = error
    cls.warn = warn
    cls.debug = debug
    cls.note = note
    cls.log = log
    ui.log("logging",
           "Diverted all output to the standard Python logging module")
