#!/usr/bin/env python3

## Include Files Here

import time
import os, sys
from lib import com
import rescue as r

from menu import TextMenu
from rescue import Recovery

## Functions
def colorPrint(txt,colorStart):
	print(colorStart+txt+'\033[0m') # Print in color then reset color on end of line.

# Variable definistions
_sleep_ = 5
MyOS = com._OS_()


## Menu dictionaries
MainMenu_Headers = ["","Run","Description"]
MainMenu_Items = {"1":["GsmartControl","Harddrive Diagnostics"],
                  "2":["GNU ddrescue","Hard drive recovery + sector cloning"],
                  "3":["Rsync","Backup file systems to drive or server"],
                  "4":["Chntpw","Offline Windows password reset"],
                  "Q":["Quit","Closes terminal window"],
                  "S":["Shutdown","Power down System"],
                  "R":["Reboot","Reboot system (warm boot)"]}

RecoveryTypeMenu_Headers = ["","Type","Description"]
RecoveryTypeMenu_Items = {'1':["Full", "Copy passes x3, trim, and scrape"],
                          '2':["No Scrape","Copy passes x3 with trim only"],
                          '3':["No Trim","Copy passes x3, no trim, no scrape"],
                          '4':["Clone","Copy passes x1 with a larger read size"],
                          'R':["Restart", "Restarts the Recovery Setup Wizard"],
                          'B':["Back", "Back to main menu"]}
### Build the menues ###
MainMenu = TextMenu(MainMenu_Items,MainMenu_Headers)
RecoveryTypeMenu = TextMenu(RecoveryTypeMenu_Items)

MainMenu.Align(MainMenu_Headers[1],"l")
MainMenu.Align(MainMenu_Headers[2],"l")
RecoveryTypeMenu.Align(RecoveryTypeMenu_Headers[1],"l")
RecoveryTypeMenu.Align(RecoveryTypeMenu_Headers[2],"l")
## Functions ##
def ForkRecovery():
    pid = os.fork()
    if pid:
    # we are the parent
        os.close(w) # use os.close() to close a file descriptor
        print(com.color.OKGREEN+'ddrescue '+RecoverDisk+' '+TargetDisk+' '+LogFile+com.color.END)
        DoRescue(LogFile, RecoverDisk, TargetDisk, _DD_OPTIONS_)
        os.waitpid(pid, 0) # make sure the child process gets cleaned up
    
    else:
    # we are the child
        os.close(r)
        Popen(['ddrescueview', RescueLogPath+"/"+LogFile], stdout=PIPE, stderr=PIPE)
        sys.exit(0)

def SetUpRescue():
        MyOS.Clear()
        Task = Recovery()
        TaskOptions = Task.GetConfigFromUser()
        TaskOptions['LogFile'] = Task.GetLogName()
        RecoveryTypeMenu.Print()

        for case in com.switch(input('Recovery Type []: ').lower()):
            print("\n\n") # padd down a few lines then print selected options.
            if case('1'):
                print("Full: {}".format(Task.Type("full")))
                break
            if case('2'): # No Scrape
                print("No Scrape Recovery selected.")
                break
            if case('3'): # No trim
                print("Full 3 pass clone selected.")
                break
            if case('4'): # Single forward copy (large block size) good drive clone
                print("Single pass Clone selected.")
                break
            if case('r'):# Restarts the Recovery Setup
                break
            if case('b'):
                print("Back to main Menu")
                break
            if case(): # default
                print("Please make a valid selection.")
			# restart the prompts

        print("Selected Options."+com.color.OKBLUE)
        print(com.color.END+com.color.WARNING+"Executing ddrescue."+com.color.END)


def main():
    while True:
        MyOS.Clear()
        colorPrint("Diagnostic and Recovery Programs",com.color.HEADER)
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
                SetUpRescue()
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
                MyOS.Reboot()
                break

# start program here
if __name__ == "__main__":
    main()