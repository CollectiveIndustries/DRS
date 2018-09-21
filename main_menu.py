#!/usr/bin/env python3

## Include Files Here

import time
import os
from lib import com



## Functions
def colorPrint(txt,colorStart):
	print(colorStart+txt+'\033[0m') # Print in color then reset color on end of line.

# Text output color definitions
class color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# This class provides the functionality we want. You only need to look at
# this if you want to know how this works. It only needs to be defined
# once, no need to muck around with its internals.
# Located at http://code.activestate.com/recipes/410692/
class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args:
            self.fall = True
            return True
        else:
            return False

# Variable definistions
Question = None
_sleep_ = 5
MyOS = com._OS_()

while Question is None:
    MyOS.Clear()

    colorPrint("Diagnostic and Recovery Programs",color.HEADER)
    print("(A) GsmartControl - Harddrive Diagnostics.")
    print("(B) Ddrescue - Hard drive recovery + sector cloning.")
    print("(C) Rsync - Backup file systems to drive or server.")
    print("(D) Chntpw - Offline Windows password reset.")
    print("\n--------------------------------------------------------\n")
    print("(Q) Quit - Closes terminal window")
    print("(S) Shutdown - Power down system")
    print("(R) Reboot - Reboot system (warm boot)")
    print("")

    for case in switch(input("Select: ").lower()):
        if case("a"):
            print("Running gsmart hdd diagnostics.")
            time.sleep(_sleep_)
            break
        if case("b"):
            print("Calling ddrescue.")
            time.sleep(_sleep_)
            break
        if case("c"):
            print("Running rsync backup.")
            time.sleep(_sleep_)
            break
        if case("d"):
            print("Starting Offline Regedit.")
            time.sleep(_sleep_)
            break
        if case("q"):
            exit(0)
        if case("s"):
            print("Shutting down system")
            time.sleep(_sleep_)
            MyOS.Shutdown()
            break
        if case("r"):
            print("Rebooting system")
            time.sleep(_sleep_)
            MyOS.Shutdown()
            break
