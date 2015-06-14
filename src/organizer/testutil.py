#!/usr/bin/env python

'''Natures detector tests.'''

import decorator
import errno
import os
import shutil
import tempfile

@decorator.contextmanager
def dirtest():
    tempd = tempfile.mkdtemp()
    try:
        yield tempd
    finally:
        shutil.rmtree(tempd)

@decorator.contextmanager
def dirtree(paths):
    with dirtest() as d:
        for p in paths:
            dname = os.path.dirname(p)
            if dname:
                try:
                    os.makedirs(os.path.join(d, dname))
                except OSError, e:
                    if e.errno != errno.EEXIST:
                        raise
            file(os.path.join(d, p), "wb").write("")
        yield d
