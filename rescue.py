#!/usr/bin/env python3

# Python script to set variables and call ddrescue.

import ctypes
import os, sys
import shlex
import json
from subprocess import STDOUT,  PIPE, Popen, check_output, CalledProcessError
import time
from datetime import date
from lib import com

# Mount options for the CIFS server share
RescueMount = ['mount', '-o', 'username=root,password=cw8400,nocase', '//nas/data','/media/data']

# Block listing with json format so we can parse the device list
block_list = ['lsblk', '--json', '--noheadings', '--nodeps', '-o', 'name,size,model,serial,fstype']

# file system repair after the clone or rescue we need to reset bad blocks and journal files.
NtfsFix = ['ntfsfix', '--clear-bad-sectors', '--clean-dirty']

    # Make Directory Path just incase it doesnt exist
MkDir = ['mkdir','-p']
FSIgnore = ['iso9660', 'squashfs']

def doMount():
    try:
        print("Mounting Storage Server....")
        err = check_output(RescueMount)
        print(com.color.OKGREEN+"Server Drive Mounted."+com.color.END)
        time.sleep(10)
    except CalledProcessError as ERROR:
        print(com.color.FAIL+"ERROR while mounting "+RescueMount[3]+'\nReturned with Error:\n>>>> '+str(ERROR)+com.color.END)
        exit(ERROR.returncode)

class Rescue(object):
    """Defines a Recovery Object"""
    _today_ = date.today().strftime("%m-%d-%y")
    _logfmtstr_ = "RecoveryLog_{}-{}_{}_{}.frds" # RecoveryLog_LastName-FirstName_M-D-Y_TI.frds

    _recoveryType_ = {'full':['reopen-on-error', '--idirect', '--odirect', '--force', '--verbose']
                      }

    _config_ = {'cluster-size':'1024',
              'skip-size':'128s,1M',
              'CustomerFirstName':None,
              'CustomerLastName':None,
              'TechInitials':None,
              'RecoveryDisk':'/dev/sda',
              'TargetDisk':None,
              'LogPath':'/media/data/DDRescue_Logs',
              'LogFile':''
              }

    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)

    def _DisplayConfigChanges(self,_newConf_):
        """Prints out a side by side view of the configuration settings"""
        _frmtstr_ = "{} {} --> {} {}"
        for k,v in self._config_.items():
            print(_frmtstr_.format( k,v,1,2 ) )

    def GetLogName(self):
        """Returns formated log name"""
        return self._logfmtstr_.format(self._GetConfig('CustomerLastName'),self._GetConfig('CustomerFirstName'),self._today_,self._GetConfig('TechInitials'))

    def SetConfig(self,name,value):
        """Saves value to name"""
        self._config_[name] = value

    def _saveConfig(self,_newConfig_):
        """Saves the user settings"""
        self._config_ = _newConfig_

    def GetConfigFromUser(self):
        """Gets data from user to define recovery environment"""
        confirm = "{}Using Target{} \"{}\" Are you sure (y/n)?"
        UserOptions = self._config_
        UserOptions['TargetDisk'] = ''

        UserOptions['RecoveryDisk'] = input("{}Disk to recover (defualt marked in []):{} [ {} ] ".format(com.color.HEADER, com.color.END,self._GetConfig('RecoveryDisk')))
    
        while True:
            UserOptions['TargetDisk'] = input("{}Target Drive:{} [ {} ] ".format(com.color.HEADER, com.color.END,self._GetConfig('TargetDisk')))

            if UserOptions['TargetDisk'] == "":
                print("{}Target cannot be empty{}".format(com.color.FAIL,com.color.END))
            elif input(confirm.format(com.color.WARNING, com.color.END, UserOptions['TargetDisk'])) == "y":
                break
    
        print("\nThe following numbers may be in decimal, hexadecimal or octal, and may be followed by\na multiplier: s = sectors, k = 1000, Ki = 1024, M = 10^6,  Mi  =  2^20, etc")
    
        UserOptions['skip-size'] = input("{}Skip Size (min,max):{} [ {} ] ".format(com.color.HEADER, com.color.END,self._GetConfig('skip-size')))
        UserOptions['cluster-size'] = input("{}Cluster Size:{} [ {} ] ".format(com.color.HEADER, com.color.END,self._GetConfig('cluster-size')))
        UserOptions['TechInitials'] = input("{}Technitian Initals:{} [ {} ] ".format(com.color.HEADER, com.color.END,self._GetConfig('TechInitials')))

        self._DisplayConfigChanges(UserOptions)

        return UserOptions

    def _GetConfig(self,name):
        """Gets value by name"""
        return self._config_[name]



def DoRescue(LogFile, RecoverDisk, TargetDisk, _DD_OPTIONS_):
    try:
        rescue = Popen(['ddrescue']+_DD_OPTIONS_+[RecoverDisk,TargetDisk,RescueLogPath+"/"+LogFile],  stderr=PIPE)
    except:
        print("Error trying to call rescue")

def PrintLSBLK():
       lsblk = Popen(block_list, stdout=PIPE, stderr=PIPE)
       out, err = lsblk.communicate()
       try:
           decoded = json.loads(out)
    
    # Access data
           for x in decoded['blockdevices']:
               if x['fstype'] not in FSIgnore: # Make sure we list only valid drives and are NOT in the Ignore list
                   print(com.color.HEADER+"Drive:  "+com.color.OKGREEN+"/dev/"+x['name']+com.color.END)
                   print(com.color.HEADER+"Size:   "+com.color.WARNING+x['size']+com.color.END)
               if x['model'] is not None:
                   print(com.color.HEADER+"Model:  "+com.color.END+x['model'])
               if x['serial'] is not None:
                   print(com.color.HEADER+"Serial: "+com.color.END+x['serial'])
               print("") # add a blank line at the end of each group as some values may not print
    
       except (ValueError, KeyError, TypeError):
           print("lsblk returned the wrong JSON format")



def rescue():
# Clear screen
        
        os.system("clear")
        myobject = Rescue()

        print(com.color.BOLD+"\nAttached Storage Devices.\n"+com.color.END)
        
        
        UserOptions = myobject.GetConfigFromUser()
        UserOptions['LogFile'] = myobject.GetLogName()
        


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
