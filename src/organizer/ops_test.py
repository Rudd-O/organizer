#!/usr/bin/python3

"""Operators tests."""

import contextlib
from organizer import ops
from . import testutil
import unittest

class CapturedCommandTest(unittest.TestCase):

    def setUp(self):
        self.commands = []

    def call(self, *args):
        self.commands.append(args[0])
        return 0

    @contextlib.contextmanager
    def patch_calls(self):
        old_call = ops.call
        old_check_call = ops.check_call
        try:
            ops.call = self.call
            ops.check_call = self.call
            yield
        finally:
            ops.call = old_call
            ops.check_call = old_check_call

class CLIOperatorTest(CapturedCommandTest):

    def test_simple_ops(self):
        with self.patch_calls():
            o = ops.CLIOperator()
            o.create_directories("/a")
            o.take_ownership("/b/c/d")
            o.move_file("/b/c/d", "/a")
        self.assertListEqual(self.commands, [
            "mkdir -p -- /a".split(),
            "takeown -r -- /b/c/d".split(),
            "mv -iT -- /b/c/d /a".split(),
        ])

class KIOOperatorTest(CapturedCommandTest):

    def test_simple_ops(self):
        with self.patch_calls():
            o = ops.KIOOperator()
            o.create_directories("/a")
            o.take_ownership("/b/c/d")
            o.move_file("/b/c/d", "/a")
        self.assertListEqual(self.commands, [
            "mkdir -p -- /a".split(),
            "takeown -r -- /b/c/d".split(),
            "kde-mv -- /b/c/d /a".split(),
        ])

    def test_destfile_exists(self):
        with testutil.dirtest() as d:
            with self.patch_calls():
                o = ops.KIOOperator()
                o.take_ownership("/b/c/d")
                o.move_file("/b/c/d", d)
            self.assertListEqual(self.commands, [
                "takeown -r -- /b/c/d".split(),
                ["kdialog", "--warningyesno", "File /b/c/d will replace %s.  Are you sure?" % d],
                ("rm -rf -- %s" % d).split(),
                ("kde-mv -- /b/c/d %s" % d).split(),
            ])
