# Copyright 2019-2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License_indentifier: GPL-2.0-or-later
import logging

CONFIG_SECTION = 'logging'
DEFAULT_GENERAL_FORMAT = (
    "[%(asctime)s] [%(process)d] [%(levelname)s] [%(name)s] %(message)s"
)
DEFAULT_HG_FORMAT = (
    "[%(asctime)s] [%(process)d] [%(levelname)s] "
    "repo:%(repo)s "
    "[%(name)s] %(message)s"
)


def loglevel(levelname):
    """A converter from string representation.

    This is meant to be usable with `ui.configwith`.
    """
    return getattr(logging, levelname.strip().upper())
