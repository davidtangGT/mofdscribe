# -*- coding: utf-8 -*-
"""Utils for MOFDescribe."""

import sys
from shutil import which

if sys.version_info.major == 3 and sys.version_info.minor >= 10:
    from collections.abc import MutableMapping
else:
    from collections import MutableMapping


def is_tool(name):
    """Check whether `name` is on PATH and marked as executable.

    https://stackoverflow.com/questions/11210104/check-if-a-program-exists-from-a-python-script"""

    return which(name) is not None


def flatten(d: dict, parent_key: str = "", sep: str = ".") -> dict:
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)
