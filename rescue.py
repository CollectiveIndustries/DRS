#!/usr/bin/env python3

# Python script to set variables and call ddrescue.

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


class Recovery(object):
    """Defines a Recovery Environment Object"""
    _today_ = date.today().strftime("%m-%d-%y")
    _logfmtstr_ = "RecoveryLog_{}-{}_{}_{}.frds" # RecoveryLog_LastName-FirstName_M-D-Y_TI.frds
    _FSIgnore_ = ['iso9660', 'squashfs']

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

    def doMount(): # Needs refactoring (move to class Recovery()
        try:
            print("Mounting Storage Server....")
            err = check_output(RescueMount)
            print(com.color.OKGREEN+"Server Drive Mounted."+com.color.END)
            time.sleep(10)
        except CalledProcessError as ERROR:
            print(com.color.FAIL+"ERROR while mounting "+RescueMount[3]+'\nReturned with Error:\n>>>> '+str(ERROR)+com.color.END)
            exit(ERROR.returncode)

    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)

    def _DisplayConfigChanges(self,_newConf_={}):
        """Prints out a side by side view of the configuration settings"""
        _frmtstr_ = "{}: {} --> {}"
        for k,v in self._config_.items():
            for _k_, _v_ in _newConf_.items():
                if k == _k_:
                    print(_frmtstr_.format( k,v,_v_) )

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

        UserOptions = self._config_

        UserOptions['RecoveryDisk'] = input("{}Disk to recover (defualt marked in []):{} [ {} ] ".format(com.color.HEADER, com.color.END,self._GetConfig('RecoveryDisk')))
    
        print("\nThe following numbers may be in decimal, hexadecimal or octal, and may be followed by\na multiplier: s = sectors, k = 1000, Ki = 1024, M = 10^6,  Mi  =  2^20, etc")
    
        UserOptions['skip-size'] = input("{}Skip Size (min,max):{} [ {} ] ".format(com.color.HEADER, com.color.END,self._GetConfig('skip-size')))
        UserOptions['cluster-size'] = input("{}Cluster Size:{} [ {} ] ".format(com.color.HEADER, com.color.END,self._GetConfig('cluster-size')))


        UserOptions['TargetDisk'] = self.GetInputNonEmpty("Target Disk")

        while not self.Confirm("Target Disk", UserOptions['TargetDisk']):
            UserOptions['TargetDisk'] = self.GetInputNonEmpty("Target Disk")
        
        # Cannot be left blank these control the log file format
        UserOptions['TechInitials'] = self.GetInputNonEmpty("Tech Initials")
        UserOptions['CustomerLastName'] = self.GetInputNonEmpty("Customer Last Name")
        UserOptions['CustomerFirstName'] = self.GetInputNonEmpty("Customer First Name")

        self._DisplayConfigChanges(UserOptions)

        return UserOptions

    def _GetConfig(self,name):
        """Gets value by name"""
        return self._config_[name]

    def DoRecovery(self):
        """Calls ddrescue with the current configuration"""
        try:
            rescue = Popen([],  stderr=PIPE)
        except:
            print("Error trying to call rescue")

    def GetDevices(): # needs refactoring
        """Get devices from lsblk"""
        print(com.color.BOLD+"\nAttached Storage Devices.\n"+com.color.END)
        lsblk = Popen(block_list, stdout=PIPE, stderr=PIPE)
        out, err = lsblk.communicate()
        try:
            decoded = json.loads(out)
            for x in decoded['blockdevices']:
                if x['fstype'] not in self._FSignore_: # Make sure we list only valid drives and are NOT in the Ignore list
                    print(com.color.HEADER+"Drive:  "+com.color.OKGREEN+"/dev/"+x['name']+com.color.END)
                    print(com.color.HEADER+"Size:   "+com.color.WARNING+x['size']+com.color.END)
                if x['model'] is not None:
                    print(com.color.HEADER+"Model:  "+com.color.END+x['model'])
                if x['serial'] is not None:
                    print(com.color.HEADER+"Serial: "+com.color.END+x['serial'])
                    print("") # add a blank line at the end of each group as some values may not print
    
        except (ValueError, KeyError, TypeError):
            print("lsblk returned the wrong JSON format")
