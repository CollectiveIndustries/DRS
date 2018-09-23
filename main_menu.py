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

colorPrint("Diagnostic and Recovery Programs",com.color.HEADER)
MainMenu = Menu(MainMenu_Items)


while True:
    MyOS.Clear()
    print("OS Detected: {}".format(MyOS.FormatName()))
    MainMenu.Print()

    case = MenuInput()


def rescue():
# Clear screen
        
        os.system("clear")
        Task = Recovery()
        
        TaskOptions = Task.GetConfigFromUser()
        TaskOptions['LogFile'] = Task.GetLogName()

        print("\n"+com.color.HEADER+"Recovery type:"+com.color.END+"\nA) Full (runs 3 copy passes, trim, and scrape)\nB) No Scrape (Copy X3, trim)\nC) No Trim (just the copy passes)\nD) Clone (copy pass 1 with a larger read size)\n\nR) Restart\nQ) Quit")

        # Empty suites are considered syntax errors, so intentional fall-throughs
	    # should contain 'pass'
        for case in com.switch(input('Recovery Type []: ').lower()):
            print("\n\n") # padd down a few lines then print selected options.
            if case('a'): # Full recovery
			#
                _DD_OPTIONS_ = ['--cluster-size='+ClusterSize, '--skip-size='+SkipSize, '--reopen-on-error', '--idirect', '--odirect', '--force', '--verbose']
                print("Full Recovery selected.")
                Question = ''
                break
            if case('b'): # No Scrape
			#
                _DD_OPTIONS_ = ['--cluster-size='+ClusterSize, '--skip-size='+SkipSize, '--reopen-on-error', '--idirect', '--odirect', '--force', '--verbose', '--no-scrape']
                print("No Scrape Recovery selected.")
                Question = ''
                break
            if case('c'): # No trim
			#
                _DD_OPTIONS_ = ['--cluster-size='+ClusterSize, '--skip-size='+SkipSize, '--reopen-on-error', '--idirect', '--odirect', '--force', '--verbose', '--no-scrape', '--no-trim']
                print("Full 3 pass clone selected.")
                Question = ''
                break
            if case('d'): # Single forward copy (large block size) good drive clone
			#
                _DD_OPTIONS_ = ['--cluster-size='+ClusterSize, '--cpass=1', '--idirect', '--odirect', '--force', '--verbose', '--no-trim', '--no-scrape']
                print("Single pass Clone selected.")
                Question = ''
                break
            if case('r'): break

            if case('q'):
                print("Program Terminated")
                exit(0) #normal program termination

            if case(): # default
                print("Please make a valid selection.")
			# restart the prompts

        print("Selected Options."+com.color.OKBLUE)
        print("\n".join(str(x) for x in _DD_OPTIONS_).replace("--", "").replace("="," = "))
        print(com.color.END+com.color.WARNING+"Executing ddrescue."+com.color.END)

        # fork the subprocess here
        r, w = os.pipe() # these are file descriptors, not file objects

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

# Full recovery will work as follows.
# 1) Run through on a full copy [cpass 1,2,3] with a larger block size (1024)
#	Skip size of 128s,1M (128 sectors up to 1 Meg)

# 2) Run a full copy with a smaller block size (128). This is a fast trim copy phase
#	size of 128s,256s (keep skip size down low to try and copy as much as possible)

# 3) 3rd run no copy, Trim and Scrape Only