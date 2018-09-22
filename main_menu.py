#!/usr/bin/env python3

## Include Files Here

import time
import os
from lib import com

## Functions
def colorPrint(txt,colorStart):
	print(colorStart+txt+'\033[0m') # Print in color then reset color on end of line.

# Variable definistions
Question = None
_sleep_ = 5
MyOS = com._OS_()

while Question is None:
    MyOS.Clear()

    print("OS Detected: {}".format(MyOS.FormatName()))
    colorPrint("Diagnostic and Recovery Programs",com.color.HEADER)
    print("(A) GsmartControl - Harddrive Diagnostics.")
    print("(B) Ddrescue - Hard drive recovery + sector cloning.")
    print("(C) Rsync - Backup file systems to drive or server.")
    print("(D) Chntpw - Offline Windows password reset.")
    print("\n--------------------------------------------------------\n")
    print("(Q) Quit - Closes terminal window")
    print("(S) Shutdown - Power down system")
    print("(R) Reboot - Reboot system (warm boot)")
    print("")

    for case in com.switch(input("Select: ").lower()):
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
