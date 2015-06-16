#!/usr/bin/env python

"""Path utilities."""

import os
from glob import glob as g

def glob(basepath, expression):
    """Properly globs even when the base path has globbing metacharacters."""
    newbasepath = []
    for c in basepath:
        if c in "*[]?":
            newbasepath.append("[")
        newbasepath.append(c)
        if c in "*[]?":
            newbasepath.append("]")
    newbasepath = "".join(newbasepath)
    return g(os.path.join(newbasepath, expression))
