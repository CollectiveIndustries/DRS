# Python script to set variables and call ddrescue.

import os, sys, shlex, time
from jproc import JSONProcess
from subprocess import STDOUT,  PIPE, Popen, check_output, CalledProcessError
from datetime import date
from lib import com
from menu import TextMenu
from prettytable import PrettyTable

MyOS = com._OS_()

global debug
debug = False
_lsblkDataFile_ = "lsblkDump.json"
if MyOS._type_ == "win32":
    debug = True

# Mount options for the CIFS server share
RescueMount = ['mount', '-o', 'username=root,password=cw8400,nocase', '//nas/data','/media/data']

# Block listing with json format so we can parse the device list
block_list = ['lsblk', '--json', '--noheadings', '--nodeps', '-o', 'name,size,model,serial,fstype']

# file system repair after the clone or rescue we need to reset bad blocks and journal files.
NtfsFix = ['ntfsfix', '--clear-bad-sectors', '--clean-dirty']

# Make Directory Path just incase it doesnt exist
MkDir = ['mkdir','-p']

class Recovery(object):
    """Defines a Recovery Task Object"""
    def __init__(self, *args, **kwargs):
        global debug
        self._today_ = date.today().strftime("%m-%d-%y")
        self._logfmtstr_ = "{}-{}_{}_{}.frds" # LastName-FirstName_M-D-Y_TI.frds
        self._FSIgnore_ = ['iso9660', 'squashfs']
    
        self._SettingsTable_ = PrettyTable()
        self._SettingsTable_.field_names = ["Option","Value"]
        self._SettingsTable_.align["Option"] = "l"
        self._SettingsTable_.align["Value"] = "l"
        
        self._recoveryType_ = {'full':['reopen-on-error', 'idirect', 'odirect', 'force', 'verbose'],
                               'noscrape':['reopen-on-error', 'idirect', 'odirect', 'force', 'verbose', 'no-scrape'],
                               'notrim':['reopen-on-error', 'idirect', 'odirect', 'force', 'verbose', 'no-scrape', 'no-trim'],
                               'clone':['idirect', 'odirect', 'force', 'verbose', 'no-trim', 'no-scrape']
                              }

        self._config_ = {'cluster-size':'1024',
                         'skip-size':'128s,1M',
                         'cpass':'3',
                         'CustomerFirstName':None,
                         'CustomerLastName':None,
                         'TechInitials':None,
                         'RecoveryDisk':'/dev/sda',
                         'TargetDisk':None,
                         'LogPath':'/log/',
                         'LogFile':''
                        }

    def _RecoveryCMDbuilder_(self,type='full'):
        """Returns recovery options based on type.
        full, noscrape, notrim, clone
        """
        frmtStrLng = "--{}={}"
        frmtStrSrt = "--{}"
        optLst = []

        clusterSize = self._config_['cluster-size']
        skipSize = self._config_['skip-size']
        copyPass = self._config_['cpass']

        for o in self._recoveryType_[type]:
            optLst += [frmtStrSrt.format(o)]

        if type == 'clone':
            return [frmtStrLng.format("cluster-size",clusterSize),frmtStrLng.format("cpass","1")] + optLst
        else:
            return [frmtStrLng.format("cluster-size",clusterSize), frmtStrLng.format("skip-size",skipSize),frmtStrLng.format("cpass",copyPass) ] + optLst

    def NasMount(): # Needs refactoring Might be moved to a NAS Storage handler
        try:
            print("Mounting Storage Server....")
            err = check_output(RescueMount)
            print(com.color.OKGREEN+"Server Drive Mounted."+com.color.END)
            time.sleep(10)
        except CalledProcessError as ERROR:
            print(com.color.FAIL+"ERROR while mounting "+RescueMount[3]+'\nReturned with Error:\n>>>> '+str(ERROR)+com.color.END)
            exit(ERROR.returncode)

    def _DisplayConfigChanges_(self,_newConf_={}):
        """Prints out a side by side view of the configuration settings"""
        self._SettingsTable_.clear_rows() # clean out the table and rebuild a new one with current settings
        for name, value in _newConf_.items():
            self._SettingsTable_.add_row([name,value])
        print(self._SettingsTable_)

    def GetLogName(self):
        """Returns formated log name"""
        return self._logfmtstr_.format(self._GetConfig('CustomerLastName'),self._GetConfig('CustomerFirstName'),self._today_,self._GetConfig('TechInitials'))

    def _userqa_(self):
        """internal method for asking user config questions"""
        UserOptions = self._config_
        MyOS.Clear()
        if debug:
            print("\n\n{}WARNING{} Win32 Debug Environment detected.\nAll ddrescue functionality disabled.\n".format(com.color.WARNING,com.color.END))

        self._GetDevices_()

        print("\nDefualts are marked in [ ]\n")
        
        UserOptions['RecoveryDisk'] = TextMenu.GetDefaults("Recovery Disk", self._GetConfig('RecoveryDisk'))
        UserOptions['cpass'] = TextMenu.GetDefaults("Number of Copy Passes",self._GetConfig('cpass'))
        print("\nThe following numbers may be in decimal, hexadecimal or octal, and may be followed by\na multiplier: s = sectors, k = 1000, Ki = 1024, M = 10^6,  Mi  =  2^20, etc")
        UserOptions['skip-size'] = TextMenu.GetDefaults("Skip Size (min,max)",self._GetConfig('skip-size'))
        UserOptions['cluster-size'] = TextMenu.GetDefaults("Cluster Size",self._GetConfig('cluster-size'))
        UserOptions['TargetDisk'] = TextMenu.GetInputNonEmpty("Target Disk")
        
        while not TextMenu.Confirm("Target Disk", UserOptions['TargetDisk']):
            UserOptions['TargetDisk'] = TextMenu.GetInputNonEmpty("Target Disk")

        # Cannot be left blank these control the log file format
        UserOptions['TechInitials'] = TextMenu.GetInputNonEmpty("Tech Initials").upper()
        UserOptions['CustomerLastName'] = TextMenu.GetInputNonEmpty("Customer Last Name").capitalize()
        UserOptions['CustomerFirstName'] = TextMenu.GetInputNonEmpty("Customer First Name").capitalize()
        UserOptions['LogFile'] = self.GetLogName()
        
        MyOS.Clear()
        self._DisplayConfigChanges_(UserOptions)
        return UserOptions

    def GetConfigFromUser(self):
        """Gets data from user to define recovery environment"""
        UserOptions = self._userqa_()
        while not TextMenu.Confirm("Configuration Changed"):
             self._userqa_()
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

    # TODO 1 EXCEPTION on json import, refactor and move to jproc module


    def _GetDevices_(self): # TODO 0 needs refactoring, this is part of Issue #1
        """Get devices from lsblk
        If Win32 OS load lsblkDump.json"""
        print(com.color.BOLD+"\nAttached Storage Devices.\n"+com.color.END)
        UserOptions = self._config_
        _FSignore_ = ['iso9660', 'squashfs']

        # Load data from provider
        if not debug:
            try:
                lsblk = Popen(block_list, stdout=PIPE, stderr=PIPE)
                out, err = lsblk.communicate()
            except OSError as _e_:
                print("{}Returned with Error:\n>>>>{}\n>>>>{}\n{}".format(com.color.FAIL,_e_.errno,_e_.strerror,com.color.END))

            try:
                json.loads(myResponse.content.decode(chardet.detect(myResponse.content)["encoding"]))
                decoded = json.loads(out)
            except (ValueError, KeyError, TypeError) as e: # LSBLK is also not in the Linux Subshell for Windows
                print("[{}FAIL{}] lsblk returned the wrong JSON format".format(com.color.FAIL,com.color.END))
                print("{}Returned with:\n>>>{}{}".format(com.color.FAIL,out,com.color.END))
                print(str(e)) # the JSON object must be str, not 'bytes'
                print("Using json dump instead!! {}WARNING{} Falling back in debug mode.".format(com.color.WARNING,com.color.END))
                decoded = self._loadJsonDump_()
        else: # LSBLK is unsupported on windows use the JSON test data from the Kali Linux VM instead
            decoded = self._loadJsonDump_()
            
        for x in decoded['blockdevices']:
            if x['fstype'] not in _FSignore_: # Make sure we list only valid drives and are NOT in the Ignore list
                print(com.color.HEADER+"Drive:  "+com.color.OKGREEN+"/dev/"+x['name']+com.color.END)
                print(com.color.HEADER+"Size:   "+com.color.WARNING+x['size']+com.color.END)
            if x['model'] is not None:
                print(com.color.HEADER+"Model:  "+com.color.END+x['model'])
            if x['serial'] is not None:
                print(com.color.HEADER+"Serial: "+com.color.END+x['serial'])
                print("") # add a blank line at the end of each group as some values may not print