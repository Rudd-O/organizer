#!/usr/bin/env python

'''Natures detector tests.'''

import os
import unittest
from organizer import natures
from organizer.testutil import dirtree

class TestDetectNature(unittest.TestCase):

    def test_simple_tvshow(self):
        nature = natures.detect_nature(
            "Greys.Anatomy.S08E14.HDTV.XviD-ENCODED.avi"
        )
        assert isinstance(nature, natures.TVShow), nature
        assert nature.subdir_hints() == ("Greys.Anatomy", "Season 8"), nature.subdir_hints()
        nature = natures.detect_nature(
            "Greys.Anatomy.Season 09 Episode 19.HDTV.XviD-ENCODED.avi"
        )
        assert isinstance(nature, natures.TVShow), nature
        assert nature.subdir_hints() == ("Greys.Anatomy", "Season 9"), nature.subdir_hints()
        nature = natures.detect_nature(
            "Greys.Anatomy.season 7 Ep 15.HDTV.XviD-ENCODED.avi"
        )
        assert isinstance(nature, natures.TVShow), nature
        assert nature.subdir_hints() == ("Greys.Anatomy", "Season 7"), nature.subdir_hints()
        nature = natures.detect_nature(
            "Doctor.Who.2005.8x03.Robot.Of.Sherwood.720p.HDTV.x264.avi"
        )
        assert isinstance(nature, natures.TVShow), nature
        assert nature.subdir_hints() == ("Doctor.Who.2005", "Season 8"), nature.subdir_hints()
        nature = natures.detect_nature(
            "Greys.Anatomy.XviD-ENCODED.avi"
        )
        assert not isinstance(nature, natures.TVShow), nature
        assert nature.subdir_hints() == (), nature.subdir_hints()

    def test_is_not_simple_tvshow(self):
        nature = natures.detect_nature(
            "Greys.Anatomy.S08E14.HDTV.XviD-ENCODED"
        )
        assert not isinstance(nature, natures.TVShow), nature

    def test_simple_movie(self):
        nature = natures.detect_nature(
            "99.F.FRENCH.ENCODED.GOOD.avi"
        )
        assert isinstance(nature, natures.Movie)
        assert nature.subdir_hints() == (), nature.subdir_hints()

    def test_simple_movie_folder(self):
        p = "99.F.FRENCH.ENCODED.GOOD/99.F.FRENCH.ENCODED.GOOD.avi"
        with dirtree([p]) as d:
            x = os.path.join(d, p)
            nature = natures.detect_nature(os.path.dirname(x))
            assert isinstance(nature, natures.MovieFolder), nature
            assert nature.subdir_hints() == (), nature.subdir_hints()
            nature = natures.detect_nature(x)
            assert isinstance(nature, natures.Movie)
            assert nature.subdir_hints() == (), nature.subdir_hints()

    def test_simple_tv_show_container(self):
        p = "Bones X/Bones S08E02.avi"
        with dirtree([p]) as d:
            x = os.path.join(d, "Bones X")
            nature = natures.detect_nature(x)
            assert nature.__class__ == natures.TVShowContainer, nature
            assert nature.path_to_organize == os.path.join(d, p), nature.path_to_organize

    def test_simple_tv_show_folder(self):
        with dirtree(["Bones X/Bones S08E02.avi",
                      "Bones X/Bones S08E02.en.srt"]) as d:
            x = os.path.join(d, "Bones X")
            nature = natures.detect_nature(x)
            assert nature.__class__ == natures.TVShowFolder, nature
            assert nature.path_to_organize == x, nature.path_to_organize

    def test_simple_album(self):
        p = [
            "Dyango/01-Superduper.mp3",
            "Dyango/02-Othersong.mp3",
        ]
        with dirtree(p) as d:
            x = os.path.join(d, "Dyango")
            nature = natures.detect_nature(x)
            assert isinstance(nature, natures.Album), nature

    def test_simple_compilation(self):
        ps = [
            ([
                "VA-somemusic/01-Superduper.mp3",
                "VA-somemusic/02-Othersong.mp3",
            ], True),
            ([
            "various.artists-somemusic/01-Superduper.mp3",
            "various.artists-somemusic/02-Othersong.mp3",
            ], True),
            ([
                "VAgine-somemusic/01-Superduper.mp3",
                "VAgine-somemusic/02-Othersong.mp3",
            ], False),
        ]
        for p, val in ps:
            with dirtree(p) as d:
                x = os.path.join(d, os.path.dirname(p[0]))
                nature = natures.detect_nature(x)
                assert isinstance(nature, natures.Compilation) == val, (nature, p)
