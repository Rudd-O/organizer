#!/usr/bin/env python

'''Natures detector tests.'''

import os
import unittest
from organizer import assistant
from organizer import natures
from organizer.testutil import createpaths, dirtree

class NoMemory(object):
    """Memory that recalls nothing."""

    def recall_destination_for_nature(self, klass):
        pass

    def recall_associated_hint(self, hint):
        pass

    def remember_destination_for_nature(self, klass, dest):
        pass

    def remember_associated_hint(self, hint, substitution):
        pass

class ChickenHead(object):
    """Memory that recalls until it forgets."""

    def __init__(self):
        self.destinations_for_nature = dict()
        self.associated_hints = dict()

    def recall_destination_for_nature(self, klass):
        return self.destinations_for_nature.get(klass)

    def recall_associated_hint(self, hint):
        return self.associated_hints.get(hint)

    def remember_destination_for_nature(self, klass, dest):
        if dest is None and klass in self.destinations_for_nature:
            del self.destinations_for_nature[klass]
        if dest is not None:
            self.destinations_for_nature[klass] = dest

    def remember_associated_hint(self, hint, substitution):
        if substitution is None and hint in self.associated_hints:
            del self.associated_hints[hint]
        if substitution is not None:
            self.associated_hints[hint] = substitution

class TestAssistant(unittest.TestCase):

    def test_assistant_with_no_memory(self):
        nomemory = NoMemory()
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

    def test_assistant_with_memory(self):
        memory = ChickenHead()
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
                a = assistant.Assistant(memory, path)
                a.begin()
                a.change_destination(d)
                for h in sethints:
                    a.change_subdir(*h)
                assert sb(a.final_path) == guess, (tname, sb(a.final_path), guess, a.subdirs)
                a.persist_in_memory()
                assert memory.destinations_for_nature == dests4nature, (tname, memory.destinations_for_nature)
                assert memory.associated_hints == assochints, (tname, memory.associated_hints)
                if sb(a.final_path):
                    createpaths(d, [sb(a.final_path)])
