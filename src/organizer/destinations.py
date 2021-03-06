#!/usr/bin/python3

'''Destinations.

This code handles possible destinations.'''

import difflib
from organizer import pathutil
import os.path

class Destination(object):

    path = None

    def __init__(self, path):
        self.path = os.path.abspath(pathutil.ensure_non_unicode(path))

    def __str__(self):
        return self.path

    def _get_hints(self, subpath):
        """Returns possible subfolders in destination."""
        path = self.path
        if subpath:
            path = os.path.join(path, subpath)
        contents = pathutil.glob(path, "*")
        contents = [ os.path.basename(p) for p in contents if os.path.isdir(p) ]
        return contents

    def guess_best_hint(self, hint, subpath=None):
        """Returns best possible subfolder based on a string hint.  May return
        None for no good hint.  Note that this does not return a full path."""
        contents = [ (x.lower(), x) for x in self._get_hints(subpath=subpath) ]
        junk = lambda x: x in ". -_"
        distances = [
            (difflib.SequenceMatcher(junk, c[0], hint.lower()).ratio(), c[1])
             for c in contents
        ]
        distances = list(sorted(distances))
        if not distances:
            return None
        shortestdistance = distances[-1]
        ratio, besthint = shortestdistance
        if ratio < 0.5:
            return None
        return besthint
