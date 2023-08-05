import os
import contextlib
from os.path import join


def rmdir_blank(path):
    """Removes folders recursively if they are empty from a
    certain path."""
    for r, d, f in os.walk(path, topdown=False):
        for folder in d:
            if len(os.listdir(join(r, folder))) == 0:
                with contextlib.suppress(Exception):
                    os.rmdir(join(r, folder))
