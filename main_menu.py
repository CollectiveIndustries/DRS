#!/usr/bin/env python

## Include Files Here
from sys import platform
import time
import os


## OS Specific Stuff
def GetOS():
    _SystemOS_ = platform.strip()
    if (_SystemOS_ == 'linux' or _SystemOS_ == 'linux2'):
    # linux
        with open('/etc/os-release') as file:
            oper = file.readlines()
            oper = oper[5].split('=')
            return oper[1].strip() # Grab OS release Name we want to know what flavor of lenny we use.
    elif(_SystemOS_ == 'win32'):
        return _SystemOS_


def OSClear(osname):
    if(osname == "win32"):
        os.system("cls")
    else: # well its not Windows we can just "clear"
        os.system("clear")

def OsInput(prompt, os):
    if(os == "win32"):
        return input(prompt)
    elif(os == "debian"):
        return raw_input(prompt)

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

## OS Specific Stuff
def GetOS():
    _SystemOS_ = platform.strip()
    if (_SystemOS_ == 'linux' or _SystemOS_ == 'linux2'):
    # linux
        with open('/etc/os-release') as file:
            oper = file.readlines()
            oper = oper[5].split('=')
            return oper[1].strip() # Grab OS release Name we want to know what flavor of lenny we use.
    elif(_SystemOS_ == 'win32'):
        return _SystemOS_
        
def OSClear(osname):
    if(osname == "win32"):
        os.system("cls")
    else: # well its not Windows we can just "clear"
        os.system("clear")
        
def OsInput(prompt, _os_):
    if(_os_ == "win32"):
        return input(prompt)
    elif(_os_ == "debian"):
        return raw_input(prompt)
   
def Shutdown(os):
	if(_OS_ == 'win32'):
		# Windows shutdown command
		os.system('shutdown', '/s')
	elif(_OS_ == 'debian'):
		# Debian shutdown command
		os.system('sudo shutdown -h')
		
def Reboot(os):
	if(_OS_ == 'win32'):
		# Windows reboot command
		os.system('shutdown', '/r')
	elif(_OS_ == 'debian'):
		# Debian reboot command
		os.system('sudo reboot')
		
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
_OS_ = GetOS()
_sleep_ = 5

while Question is None:
    OSClear(_OS_)

    colorPrint("Diagnostic and Recovery Programs",color.HEADER)
    print("(A) GsmartControl - Harddrive Diagnostics.")
    print("(B) Ddrescue - Hard drive recovery + sector cloning.")
    print("(C) Rsync - Backup file systems to drive or server.")
    print("(D) Chntpw - Offline Windows password reset.")
    print("\n--------------------------------------------------------\n")
    print("(Q) Quit - Closes terminal window")
    print("(S) Shutdown - Shuts down system")
    print("(R) Reboot - Reboot system")

    for case in switch(OsInput("Select: ",_OS_).lower()):
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
        if case("q"):
            exit(self,0)
        if case("s"):
            print("Shutting down system")
            time.sleep(_sleep_)
            ShutDown(_OS_)
            break
        if case("r"):
            print("Rebooting system")
            time.sleep(_sleep_)
            Reboot(_OS_)
            break