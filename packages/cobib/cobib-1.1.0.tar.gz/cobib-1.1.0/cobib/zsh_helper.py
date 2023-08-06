"""CoBib ZSH Helper"""

import inspect

from . import cobib
from .config import set_config


def list_commands(args=None):  # pylint: disable=unused-argument
    """ List all subcommands """
    subcommands = []
    for name, member in inspect.getmembers(cobib):
        if inspect.isfunction(member) and 'args' in inspect.signature(member).parameters:
            subcommands.append(name[:-1] + ':' + member.__doc__.split('\n')[0])
    return subcommands


def list_tags(args=None):
    """ List all tags """
    set_config(args.get('config', None))
    bib_data = cobib._read_database()  # pylint: disable=protected-access
    tags = list(bib_data.keys())
    return tags


def list_filters(args=None):
    """ List all filters """
    set_config(args.get('config', None))
    bib_data = cobib._read_database()  # pylint: disable=protected-access
    filters = set()
    for entry in bib_data.values():
        filters.update(entry.data.keys())
    return filters
