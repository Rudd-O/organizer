#!/usr/bin/env python

"""Operators.  There are operators suitable for command lines and operators
suitable for GUI usage."""

import os
import subprocess

check_call = subprocess.check_call
call = subprocess.call

def takeown(path):
    try:
        check_call(["takeown", "-r", "--", path])
    except (OSError, subprocess.CalledProcessError):
        pass

class Operator(object):
    """An Operator is a class that performs certain operations."""

    def move_file(self, original_path, new_path):
        """Moves a source file or directory into a
        destination.  Full path names are required."""
        raise NotImplementedError

    def create_directories(self, container_path):
        """Realizes the existence of container_path."""
        raise NotImplementedError

class CLIOperator(Operator):

    ops_already_performed = None

    def __init__(self):
        self.ops_already_performed = []

    def take_ownership(self, f):
        takeown(f)

    def move_file(self, original, new):
        cmd = ["mv", "-iT", "--", original, new]
        check_call(cmd)

    def create_directories(self, container):
        cmd = ["mkdir", "-p", "--", container]
        check_call(cmd)

    def remove_file(self, f):
        cmd = ["rm", "-rf", "--", f]
        check_call(cmd)

class CLIReportOperator(Operator):

    def take_ownership(self, f):
        print "Would  chown", f

    def move_file(self, original, new):
        print "        move", original
        print "          to", new
        if os.path.exists(new):
            print "   replacing", new

    def create_directories(self, container):
        print "      create", container

    def remove_file(self, f):
        print "      remove", f

class KIOOperator(CLIOperator):

    def move_file(self, original, new):
        if os.path.isdir(new):
            cmd = ["kdialog", "--warningyesno",
                   "File %s will replace %s.  Are you sure?" % (original, new)]
            ret = call(cmd)
            if ret != 0:
                return
            check_call(["rm", "-rf", "--", new])
        cmd = [
               "kde-mv",
               "--",
               original,
               new,
        ]
        check_call(cmd)
