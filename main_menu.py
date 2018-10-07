#!/usr/bin/env python3

## Include Files Here
import os, sys, time, math
import test
from lib import com
from menu import TextMenu
from rescue import Recovery
import fddrescue as fddr

## Functions
def colorPrint(txt,colorStart):
	print(colorStart+txt+'\033[0m') # Print in color then reset color on end of line.

# Variable definistions
DELAY = 5
MyOS = com._OS_()


## Menu dictionaries
MainMenu_Headers = ["#","Run","Description"]
MainMenu_Items = {"1":["GsmartControl","Harddrive Diagnostics"],
                  "2":["GNU ddrescue","Hard drive recovery + sector cloning"],
                  "3":["Rsync","Backup file systems to drive or server"],
                  "4":["Chntpw","Offline Windows password reset"],
                  "T":["Test Python","Runs a method directly for developing"],
                  "F":["Factorize","Get Prime factors for Inuput"],
                  "Q":["Quit","Closes terminal window"],
                  "S":["Shutdown","Power down System"],
                  "R":["Reboot","Reboot system (warm boot)"]}

RecoveryTypeMenu_Headers = ["#","Type","Description"]
RecoveryTypeMenu_Items = {'1':["Full", "Copy passes x3, trim, and scrape"],
                          '2':["No Scrape","Copy passes x3 with trim only"],
                          '3':["No Trim","Copy passes x3, no trim, no scrape"],
                          '4':["Clone","Copy passes x1 with a larger read size"],
                          'R':["Restart", "Restarts the Recovery Setup Wizard"],
                          'B':["Back", "Back to main menu"]}
### Build the menues ###
MainMenu = TextMenu(MainMenu_Items,MainMenu_Headers)
RecoveryTypeMenu = TextMenu(RecoveryTypeMenu_Items,RecoveryTypeMenu_Headers)

MainMenu.Align(MainMenu_Headers[1],"l")
MainMenu.Align(MainMenu_Headers[2],"l")
RecoveryTypeMenu.Align(RecoveryTypeMenu_Headers[1],"l")
RecoveryTypeMenu.Align(RecoveryTypeMenu_Headers[2],"l")

## Functions ##
def ForkRecovery(): ## Refactor This ##
    """Fork recovery process"""
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

def StartRescueTask():
    """Starts a rescue task"""
    Task = Recovery()
    InvalidResponse = True
    while True and InvalidResponse:
        MyOS.Clear()
        TaskOptions = Task.GetConfigFromUser()
        TaskOptions['LogFile'] = Task.GetLogName()
        RecoveryTypeMenu.Print()
        for case in com.switch(TextMenu.GetInputNonEmpty('Recovery Type []: ').lower()):
            print("\n\n") # padd down a few lines then print selected options.
            if case('1'):
                print("Full: {}".format(Task._RecoveryCMDbuilder_("full")))
                InvalidResponse = False
                break
            if case('2'): # No Scrape
                print("No Scrap: {}".format(Task._RecoveryCMDbuilder_("noscrape")))
                InvalidResponse = False
                break
            if case('3'): # No trim
                print("No Trim: {}".format(Task._RecoveryCMDbuilder_("notrim")))
                InvalidResponse = False
                break
            if case('4'): # Single forward copy (large block size) good drive clone
                print("Clone: {}".format(Task._RecoveryCMDbuilder_("clone")))
                InvalidResponse = False
                break
            if case('r'):# Restarts the Recovery Setup
                break
            if case('b'):
                print("Back to main Menu")
                InvalidResponse = False
                break
    time.sleep(DELAY)

def main():
    """Main program entry point"""
    while True:
        MyOS.Clear()
        colorPrint("Diagnostic and Recovery Programs",com.color.HEADER)
        print("OS Detected: {}".format(MyOS.FormatName()))

        MainMenu.Print()
        for case in com.switch(input("Select: ").lower()):
            if case("t"):
                print("Running Test module")
                time.sleep(DELAY)
                fddr.RecoverDirTree("/var/log","/mnt/d/NEWPATH")
                sys.exit()
                break
            if case("1"):
                print("Running gsmart hdd diagnostics.")
                time.sleep(DELAY)
                break
            if case("2"):
                print("Calling ddrescue.")
                time.sleep(DELAY)
                StartRescueTask()
                break
            if case("3"):
                print("Running rsync backup.")
                time.sleep(DELAY)
                break
            if case("4"):
                print("Starting Offline Regedit.")
                time.sleep(DELAY)
                break
            if case("q"):
                sys.exit()
            if case("s"):
                print("Shutting down system")
                time.sleep(DELAY)
                MyOS.Shutdown()
                break
            if case("r"):
                print("Rebooting system")
                time.sleep(DELAY)
                MyOS.Reboot()
                break

# start program here
if __name__ == "__main__":
    main()