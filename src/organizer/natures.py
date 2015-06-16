#!/usr/bin/env python

'''Natures detector.

This code detects the nature of a file path.'''

import itertools
import re
import os.path
import pathutil

MOVIE_EXTS = [".avi", ".mkv", ".mov", ".mp4"]
MUSIC_EXTS = [".ogg", ".flac", ".mp3", ".aac", ".m4a"]

def _all_natures():
    for klass in globals().values():
        if klass == Nature:
            continue
        try:
            isnature = issubclass(klass, Nature)
            if not isnature:
                continue
        except TypeError:
            continue
        yield klass

def detect_nature(path):
    """Returns a class instance of the nature of the path passed to this
    function."""
    couldbe = []
    for klass in _all_natures():
        confidence = klass.examine(path)
        couldbe.append((confidence, klass))
    itis = list(sorted(couldbe))[-1]
    return itis[1](path)

class Nature(object):

    path = None

    def __init__(self, path):
        """Instantiates a Nature object that is bound to the path passed to
        it.  This path must exist, otherwise errors may take place during
        organization."""
        self.path = path

    @classmethod
    def examine(klass, path):
        """Takes a path, and returns a value representing how confident this
        class is that it can represent the path during the organization
        process, between 0.0 and 1.0."""
        raise NotImplementedError

    def subdir_hints(self):
        """Returns an iterable (name hint, subhint) that hints to the
        classifier how to construct a classification.  The iterable may be
        zero length."""
        return ()

    def name(self):
        return self.__class__.__name__

    @property
    def path_to_organize(self):
        """Returns the actual path to organize.  If this differs from the path
        associated with this nature, that implicitly means that after
        organization of the path returned here, the path associated with
        this nature must be removed."""
        return self.path

def find_videos_within_folder(folder):
    videos = []
    contained = pathutil.glob(folder, "*")
    for c in contained:
        _, ext = os.path.splitext(c)
        if ext.lower() in MOVIE_EXTS:
            videos.append(c)
    return videos

def find_subtitles_within_folder(folder):
    contained = pathutil.glob(folder, "*.[sS][rR][tT]")
    contained2 = pathutil.glob(folder, os.path.join("*", "*.[sS][rR][tT]"))
    return contained + contained2

class TVShow(Nature):

    seasonres = [
                 r"^(.*).S(eason)?[. ]*([0-9]+)\s*E(p(isode)?)?[. ]*([0-9]+)",
                 r"^(.*)(.)([0-9]+)x([0-9][0-9]+)",
    ]

    def __init__(self, path):
        Nature.__init__(self, path)

    @classmethod
    def examine(klass, path):
        confidence = 0.0
        _, ext = os.path.splitext(path)
        if ext.lower() not in MOVIE_EXTS:
            return confidence
        confidence += 0.2
        for seasonre in klass.seasonres:
            season = re.findall(seasonre, os.path.basename(path), re.I)
            if season: break
        if season:
            confidence += 0.6
        return confidence

    def subdir_hints(self):
        base = os.path.basename(self.path)
        for seasonre in self.seasonres:
            partitioned = re.findall(seasonre, base, re.I)
            if partitioned: break
        if partitioned:
            firstmatch = partitioned[0]
            showname = firstmatch[0]
            season = "Season %d" % int(firstmatch[2])
            return (showname, season)
        return (os.path.splitext(base)[0],)

    def name(self):
        return "TV show"

class TVShowContainer(TVShow):

    def __init__(self, path):
        TVShow.__init__(self, path)
        # Must save this datum now, else path_to_organize() will bomb
        # once video is deleted.
        # This cannot fail because of the invariant that examine() is always
        # called once with the same argument before __init__() is.
        videos = find_videos_within_folder(self.path)
        self._path_to_organize = videos[0]

    @classmethod
    def examine(klass, path):
        confidence = 0.0
        videos = find_videos_within_folder(path)
        if len(videos) != 1:
            return confidence
        confidence += 0.2
        for seasonre in klass.seasonres:
            season = re.findall(seasonre, os.path.basename(videos[0]), re.I)
            if season: break
        if season:
            confidence += 0.4
        return confidence

    def subdir_hints(self):
        for seasonre in self.seasonres:
            partitioned = re.findall(seasonre, os.path.basename(self._path_to_organize), re.I)
            if partitioned: break
        if partitioned:
            firstmatch = partitioned[0]
            showname = firstmatch[0]
            season = "Season %d" % int(firstmatch[2])
            return (showname, season)
        return (os.path.splitext(videos[0])[0],)

    def name(self):
        return "Folder containing a TV show"

    @property
    def path_to_organize(self):
        return self._path_to_organize

class TVShowFolder(TVShowContainer):

    @classmethod
    def examine(klass, path):
        confidence = TVShowContainer.examine(path)
        if find_subtitles_within_folder(path):
            confidence += 0.2
        return confidence - 0.1

    def name(self):
        return "TV show folder"

    @property
    def path_to_organize(self):
        return self.path

class Movie(Nature):

    def __init__(self, path):
        Nature.__init__(self, path)

    @classmethod
    def examine(klass, path):
        confidence = 0.0
        _, ext = os.path.splitext(path)
        if ext.lower() not in MOVIE_EXTS:
            return confidence
        confidence += 0.5
        return confidence

    def subdir_hints(self):
        return ()

    def name(self):
        return "Movie file"

class MovieFolder(Nature):

    def __init__(self, path):
        Nature.__init__(self, path)

    @classmethod
    def examine(klass, path):
        confidence = 0.0
        videos = find_videos_within_folder(path)
        if len(videos) not in [1, 2]:
            return confidence
        confidence = 0.4
        if find_subtitles_within_folder(path):
            confidence = confidence + 0.3
        return confidence

    def subdir_hints(self):
        return ()

    def name(self):
        return "Movie folder"

class Album(Nature):

    def __init__(self, path):
        Nature.__init__(self, path)

    @classmethod
    def examine(klass, path):
        confidence = 0.0
        contained = itertools.chain(
            pathutil.glob(path, "*"),
            pathutil.glob(path, os.path.join("*", "*")),
        )
        for c in contained:
            _, ext = os.path.splitext(c)
            if ext.lower() in MUSIC_EXTS and confidence < 0.7:
                confidence = confidence + 0.2
        return confidence

    def name(self):
        return "Music album"

class Compilation(Nature):

    def __init__(self, path):
        Nature.__init__(self, path)

    @classmethod
    def examine(klass, path):
        confidence = Album.examine(path)
        if confidence >= 0.05:
            confidence = confidence - 0.05
            va = re.findall(r"^(VA[._-]|Various[._-]Artists)", os.path.basename(path), re.I)
            if va:
                confidence = confidence + 0.1
        return confidence

    def name(self):
        return "Music compilation"

class Unknown(Nature):

    def __init__(self, path):
        Nature.__init__(self, path)

    @classmethod
    def examine(klass, path):
        return 0.01
