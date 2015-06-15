#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Organizer program.
'''

import argparse
from organizer import assistant
from organizer import memory
from organizer import ops
import os
import sys
import traceback

QUIT = "user requested quit"

def get_parser():
    '''returns argument parser for program'''
    parser = argparse.ArgumentParser(description='Organize files into directories.')
    parser.add_argument('-b', '--batch', action="store_true", default=False,
                        help='execute entirely non-interactively -- existing files will not be replaced, while files whose destination directories do not exist or cannot be deduced wiil not be organized')
    parser.add_argument('-n', '--do-nothing', action="store_true", default=False,
                        help='do not touch files on disk -- only report putative modifications to standard output')
    parser.add_argument('files', metavar='FILES', nargs='+',
                        help='files to organize')
    return parser

def detect_gui():
    return False  # FIXME

class BatchProgram(object):

    def __init__(self, operator, mem, files):
        self.operator = operator
        self.memory = mem
        self.files = dict(
            (x, y)
            for x, y in ((os.path.abspath(f), f)
            for f in files)
        ).values()

    def mainloop(self):
        """Runs the CLI program."""
        for f in self.files:
            a = assistant.Assistant(self.memory, f)
            a.begin()
            if not a.container_of_final_path_exists:
                self.display_to_user("Skipping %s: its destination directory is nonexistent or not known" % f)
                continue
            self.operator.create_directories(a.container_of_final_path)
            self.operator.move_file(f, a.final_path)
            a.persist_in_memory()

    def display_to_user(self, msg):
        print >> sys.stdout, msg

    def display_error(self, msg):
        print >> sys.stderr, msg

class CLIProgram(BatchProgram):

    def mainloop(self):
        """Runs the CLI program."""
        for f in self.files:
            a = assistant.Assistant(self.memory, f)
            self.current_assistant = a
            a.begin()
            last_prompt = None
            while True:
                if not a.container_of_final_path:
                    self.display_to_user("The assistant needs more information to organize %s" % f)
                    self.display_to_user("Here are our best guesses:")
                else:
                    self.display_to_user("The assistant has made the following guesses for %s" % f)
                self.display_to_user("  File nature: %s" % a.nature.name())
                self.display_to_user("  Destination: %s" % a.destination)
                if a.subdirs:
                    if not a.destination:
                        self.display_to_user("  Subdirectories:")
                    for n, subdir in enumerate(a.subdirs, 1):
                        self.display_to_user("           (%s)%s└ %s" % (n, "  "*n, subdir))
                next_func = self.prompt("Change destination (d) * Change subdir (1-9) * Proceed as-is (leave blank and hit ENTER) * Quit cleanly (q)")
                if not next_func:
                    break
                last_prompt = next_func()
                if last_prompt == QUIT:
                    break
            if last_prompt != QUIT:
                if not a.container_of_final_path:
                    self.display_to_user("Skipping %s: do not know how to organize" % f)
                else:
                    self.operator.create_directories(a.container_of_final_path)
                    self.operator.move_file(f, a.final_path)
            a.persist_in_memory()
            if last_prompt == QUIT:
                break

    def quit(self):
        return QUIT

    def change_subdir(self, subdirnum):
        read = raw_input("Type the new subdirectory %s.  A blank input clears the subdirectory.\n>>> " % subdirnum)
        if not read:
            read = None
        self.current_assistant.change_subdir(subdirnum - 1, read)

    def change_destination(self):
        read = raw_input("Type the new destination path for files of this nature.  A blank input clears the destination.\n>>> ")
        if not read:
            read = None
        self.current_assistant.change_destination(read)

    def prompt(self, prompt):
        read = raw_input("%s\n>>> " % prompt)
        read = read.strip()
        try:
            readint = int(read)
            if readint < 1: raise Exception()
        except Exception:
            readint = None
        if readint is not None:
            return lambda: self.change_subdir(readint)
        elif read == "d":
            return self.change_destination
        elif read == "q":
            return self.quit
        elif read == "":
            return None
        else:
            self.display_to_user("Incorrect choice %r" % read)
            return self.prompt(prompt)

def mainloop():
    parser = get_parser()
    args = parser.parse_args()
    try:
        memcontents = file(os.path.expanduser("~/.organizer"), "rb").read()
        mem = memory.SerializableMemory.deserialize(memcontents)
    except Exception:
        mem = memory.SerializableMemory()

    gui_available = detect_gui()
    if args.batch:
        sys.stdin.close()
        gui_available = False
    if args.do_nothing:
        operator = ops.CLIReportOperator()
    else:
        if gui_available:
            operator = ops.KIOOperator()
        else:
            operator = ops.CLIOPerator()
    if args.batch:
        program = BatchProgram(operator, mem, args.files)
    else:
        if gui_available:
            pass  # FIXME            program = GUIProgram(operator, mem, args.files)
        else:
            program = CLIProgram(operator, mem, args.files)
    try:
        program.mainloop()
    except Exception, e:
        program.display_error("Unexpected exception while running: %s" % e)
        traceback.print_exc()
        return 14
    try:
        memcontents = mem.serialize()
        file(os.path.expanduser("~/.organizer"), "wb").write(memcontents)
    except Exception, e:
        program.display_error("Cannot save memory: %s" % e)
        return 18
    return 0
