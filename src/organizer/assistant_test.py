#!/usr/bin/env python

'''Assistant tests.'''

import os
import unittest
from organizer import assistant
from organizer import memory
from organizer import natures
from organizer.testutil import createpaths, dirtree

class TestAssistant(unittest.TestCase):

    def test_assistant_with_no_memory(self):
        nomemory = memory.NoMemory()
        ps = [
              (
                "GIGOLO.MARK.S01E02.avi",
                [
                 "Gigolo Mark/Season 1/mark",
                 "Gigolo Mark/Season 2/mark",
                 ],
               None,
                "Gigolo Mark/Season 1/GIGOLO.MARK.S01E02.avi",
                ),
        ]
        for fname, tree, firstguess, guess in ps:
            with dirtree(tree) as d:
                sb = lambda p: p[len(d) + 1:] if p is not None else None
                path = os.path.join(d, fname)
                a = assistant.Assistant(nomemory, path)
                a.begin()
                assert sb(a.final_path) == firstguess, (sb(a.final_path), firstguess)
                a.change_destination(d)
                assert sb(a.final_path) == guess, (sb(a.final_path), guess)

    def test_assistant_moviefolder_do_it_right(self):
        nomemory = memory.NoMemory()
        ps = [
              (
                  "Without slash",
                "Sample",
                [
                 "Sample/movie.avi",
                 ],
                [
                 "Existing/super.avi",
                 ],
                "Sample",
                ),
              (
                  "With slash",
                "Sample/",
                [
                 "Sample/movie.avi",
                 ],
                [
                 "Existing/super.avi",
                 ],
                "Sample",
                ),
        ]
        for tst, src, orgtree, dsttree, endfn in ps:
            with dirtree(orgtree) as orgd:
                with dirtree(dsttree) as dstd:
                    path = os.path.join(orgd, src)
                    a = assistant.Assistant(nomemory, path)
                    a.begin()
                    a.change_destination(dstd)
                    assert a.final_path == os.path.join(dstd, endfn), (tst, a.final_path, endfn)

    def test_assistant_tvfolder(self):
        nomemory = memory.NoMemory()
        ps = [
              (
                  "TV show with subs",
                "Sample",
                [
                 "Sample/Bones S01E01.avi",
                 "Sample/Subs/Bones.srt",
                 ],
                [
                 "somedumbfile",
                 ],
                "Bones/Season 1/Sample",
                ),
              (
                  "TV show forlorn in a folder",
                "Sample",
                [
                 "Sample/Bones S01E01.avi",
                 ],
                [
                 "somedumbfile",
                 ],
                "Bones/Season 1/Bones S01E01.avi",
                ),
        ]
        for tst, src, orgtree, dsttree, endfn in ps:
            with dirtree(orgtree) as orgd:
                with dirtree(dsttree) as dstd:
                    path = os.path.join(orgd, src)
                    a = assistant.Assistant(nomemory, path)
                    a.begin()
                    a.change_destination(dstd)
                    assert a.final_path == os.path.join(dstd, endfn), (tst, a.final_path, os.path.join(dstd, endfn))

    def test_assistant_with_memory(self):
        mem = memory.SerializableMemory()
        comprehensive = [
                         "Gigolo Mark/Season 1/mark",
                         "Gigolo Mark/Season 2/mark",
        ]
        with dirtree(comprehensive) as d:
            sb = lambda p: p[len(d) + 1:] if p is not None else None
            ps = [
                  (
                   "Test that destination hints work",
                    "GIGOLO.MARK.S01E02.avi",
                    [],
                    "Gigolo Mark/Season 1/GIGOLO.MARK.S01E02.avi",
                  {natures.TVShow: d},
                  {},
                    ),
                  (
                   "Test in the absence of destination hints that user-specified data work",
                    "ANDREW.PERALTA.S01E02.avi",
                   [(0, "Andrew Peralta")],
                    "Andrew Peralta/Season 1/ANDREW.PERALTA.S01E02.avi",
                  {natures.TVShow: d},
                  {"ANDREW.PERALTA": "Andrew Peralta"},
                    ),
                  (
                   "Test that destination hints kick in after directory has been created",
                    "ANDREW.PERALTA Season 1 Ep 4.avi",
                   [],
                    "Andrew Peralta/Season 1/ANDREW.PERALTA Season 1 Ep 4.avi",
                  {natures.TVShow: d},
                  {"ANDREW.PERALTA": "Andrew Peralta"},
                    ),
                  (
                   "Test that destination hints work even with a slightly different source file",
                    "ANDREW PERALTA Season 1 Ep 4.avi",
                   [],
                    "Andrew Peralta/Season 1/ANDREW PERALTA Season 1 Ep 4.avi",
                  {natures.TVShow: d},
                  {"ANDREW.PERALTA": "Andrew Peralta"},
                    ),
            ]
            for tname, fname, sethints, guess, dests4nature, assochints in ps:
                path = os.path.join(d, fname)
                a = assistant.Assistant(mem, path)
                a.begin()
                a.change_destination(d)
                for h in sethints:
                    a.change_subdir(*h)
                assert sb(a.final_path) == guess, (tname, sb(a.final_path), guess, a.subdirs)
                a.persist_in_memory()
                assert mem.destinations_for_nature == dests4nature, (tname, mem.destinations_for_nature)
                assert mem.associated_hints == assochints, (tname, mem.associated_hints)
                if sb(a.final_path):
                    createpaths(d, [sb(a.final_path)])
