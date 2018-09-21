#!/usr/bin/env python

## Include Files Here
from sys import platform
import time
import os


## OS Specific Stuff
class _OS_(object):
    def __init__(self):
        _SystemOS_ = platform.strip()
        if (_SystemOS_ == 'linux' or _SystemOS_ == 'linux2'):
        # linux
            with open('/etc/os-release') as file:
                oper = file.readlines()
                oper = oper[5].split('=')
                self._type_ = oper[1].strip() # Grab OS release Name we want to know what flavor of lenny we use.
        elif(_SystemOS_ == 'win32'):
            self._type_ = _SystemOS_
        
    def Clear(self):
        if(self._type_ == "win32"):
            os.system("cls")
        else: # well its not Windows we can just "clear"
            os.system("clear")

    def Input(self, prompt):
        if(self._type_ == "win32"):
            return input(prompt)
        elif(self._type_ == "debian"):
            return raw_input(prompt)

    def Shutdown(self):
        if(_OS_._type_ == 'win32'):
            os.system('shutdown', '/s')
        elif(_OS_._type_ == 'debian'):
            os.system('sudo shutdown -h')

    def Reboot(self):
        if(_OS_._type_ == 'win32'):
            os.system('shutdown', '/r')
        elif(_OS_._type_ == 'debian'):
            os.system('sudo reboot')

            ## END OF _OS_ CLASS

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
MyOS = _OS_()

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

    for case in switch(MyOS.Input("Select: ").lower()):
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