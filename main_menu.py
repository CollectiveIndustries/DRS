#!/usr/bin/env python

## Include Files Here
import os


## Functions

def colorPrint(txt,colorStart):
	print colorStart+txt+'\033[0m' # Print in color then reset color on end of line.

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

while Question is None:
	os.system("clear")
	colorPrint("Diagnostic and Recovery Programs",color.HEADER)
	print "(A) GsmartControl - Harddrive Diagnostics."
	print "(B) Ddrescue - Hard drive recovery + sector cloning."
	print "(C) Rsync - Backup file systems to drive or server."
	print "(D) Chntpw - Offline Windows password reset."

	print "\n(Q) Quit - Closes terminal window"
	print "(S) Shutdown - Shuts down system"
	print "(R) Reboot - Reboot system"
	Question = ''
