#!/usr/bin/env python3

## Include Files Here

import time
import os
from lib import com

## Functions
def colorPrint(txt,colorStart):
	print(colorStart+txt+'\033[0m') # Print in color then reset color on end of line.

# Variable definistions
_sleep_ = 5
MyOS = com._OS_()


## Menu dictionaries
MainMenu_Items = {"1":["GsmartControl","Harddrive Diagnostics."],
            "2":["GNU ddrescue","Hard drive recovery + sector cloning."],
            "3":["Rsync","Backup file systems to drive or server."],
            "4":["Chntpw","Offline Windows password reset."],
            "-1":["\n--------------------------------------------------------\n"],
            "Q":["Quit","Closes terminal window"],
            "S":["Shutdown","Power down System"],
            "R":["Reboot","Reboot system (warm boot)"]}

# Print Menu method with list of options as input
class Menu(object):
    _menuformatstring_ = "[{}] {} - {}"
    _items_ = {}

    def __init__(self,_items_=None):
        if _items_ is None:
            self._items_ = {}
        else:
            self._items_ = _items_

    def Print(self):
        for option, text in self._items_.items():
            if option != "-1":
                print(self._menuformatstring_.format(option,text[0],text[1]))
            else:
                print(text[0])

colorPrint("Diagnostic and Recovery Programs",com.color.HEADER)
MainMenu = Menu(MainMenu_Items)

while True:
    MyOS.Clear()

    print("OS Detected: {}".format(MyOS.FormatName()))
    MainMenu.Print()

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
