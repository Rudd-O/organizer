#!/usr/bin/python3

"""Path utilities."""

from glob import glob as g
import os
import sys

def glob(basepath, expression):
    """Properly globs even when the base path has globbing metacharacters."""
    newbasepath = []
    for c in basepath:
      try:
        if c in "*[]?":
            newbasepath.append("[")
        newbasepath.append(c)
        if c in "*[]?":
            newbasepath.append("]")
      except TypeError:
          assert 0, basepath
    newbasepath = "".join(newbasepath)
    return g(os.path.join(newbasepath, expression))

def ensure_non_unicode(prospectively_unicode_path):
    if isinstance(prospectively_unicode_path, bytes):
        assert 0, prospectively_unicode_path
    return prospectively_unicode_path
