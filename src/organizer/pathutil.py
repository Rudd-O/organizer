#!/usr/bin/env python

"""Path utilities."""

from glob import glob as g
import os
import sys

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

def ensure_non_unicode(prospectively_unicode_path):
    if isinstance(prospectively_unicode_path, unicode):
        prospectively_unicode_path = prospectively_unicode_path.encode(
           sys.getfilesystemencoding()
       )
    return prospectively_unicode_path
