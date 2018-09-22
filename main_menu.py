#!/usr/bin/env python3

## Include Files Here

import time
import os, sys
from lib import com
import rescue as r

## Functions
def colorPrint(txt,colorStart):
	print(colorStart+txt+'\033[0m') # Print in color then reset color on end of line.

# Variable definistions
_sleep_ = 5
MyOS = com._OS_()

## Menu dictionaries
MainMenu_Items = {"1":["GsmartControl","Harddrive Diagnostics"],
            "2":["GNU ddrescue","Hard drive recovery + sector cloning"],
            "3":["Rsync","Backup file systems to drive or server"],
            "4":["Chntpw","Offline Windows password reset"],
            "-1":["\n--------------------------------------------------------\n"],
            "Q":["Quit","Closes terminal window"],
            "S":["Shutdown","Power down System"],
            "R":["Reboot","Reboot system (warm boot)"]}

RecoveryTypeMenu_Items = {'1':["Full", "Copy passes x3, trim, and scrape"],
                          '2':["No Scrape","Copy passes x3 with trim only"],
                          '3':["No Trim","Copy passes x3, no trim, no scrape"],
                          '4':["Clone","Copy passes x1 with a larger read size"],
                          "-1":["\n--------------------------------------------------------\n"],
                          'R':["Restart", "Restarts the Recovery Setup Wizard"],
                          'B':["Back", "Back to main menu"]}


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
        if case("1"):
            print("Running gsmart hdd diagnostics.")
            time.sleep(_sleep_)
            break
        if case("2"):
            print("Calling ddrescue.")
            time.sleep(_sleep_)
            r.rescue()
            break
        if case("3"):
            print("Running rsync backup.")
            time.sleep(_sleep_)
            break
        if case("4"):
            print("Starting Offline Regedit.")
            time.sleep(_sleep_)
            break
        if case("q"):
            sys.exit()
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