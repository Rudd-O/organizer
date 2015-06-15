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

class CLIOPerator(Operator):

    ops_already_performed = None

    def __init__(self):
        self.ops_already_performed = []

    def move_file(self, original, new):
        takeown(original)
        cmd = ["mv", "-iT", "--", original, new]
        check_call(cmd)

    def create_directories(self, container):
        cmd = ["mkdir", "-p", "--", container]
        check_call(cmd)

class CLIReportOperator(Operator):

    def move_file(self, original, new):
        print "Would rename", original
        print "      to", new
        if os.path.isdir(new):
            print "      perhaps replacing existing", new

    def create_directories(self, container):
        print "Would create directories", container

class KIOOperator(Operator):

    def move_file(self, original, new):
        if os.path.isdir(new):
            cmd = ["kdialog", "--warningyesno",
                   "File %s will replace %s.  Are you sure?" % (original, new)]
            ret = call(cmd)
            if ret != 0:
                return
            check_call(["rm", "-rf", "--", new])
        takeown(original)
        cmd = [
               "kde-mv",
               "--",
               original,
               new,
        ]
        check_call(cmd)

    def create_directories(self, container):
        cmd = ["mkdir", "-p", "--", container]
        check_call(cmd)
