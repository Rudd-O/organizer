#!/usr/bin/env python

'''Natures detector tests.'''

import unittest
from organizer import destinations
from organizer.testutil import dirtree

class TestDestinations(unittest.TestCase):

    def test_dests(self):
        ps = [
              (
                "Ace.Of.Base",
                [
                 "Ace of Base/Ravine.mp3",
                 "DJ Bobo/Celebration.ogg",
                 ],
                "Ace of Base",
                ),
              (
                "Ace.Of.Base",
                [],
                None,
                ),
              (
                "Ace.Of.Base",
                [
                    "aeisrntien tsrd yukv9/asshole.mp3",
                ],
                None,
                ),
        ]
        for hint, tree, guess in ps:
            with dirtree(tree) as d:
                dest = destinations.Destination(d)
                got = dest.guess_best_hint(hint)
                assert got == guess, (got, guess)
