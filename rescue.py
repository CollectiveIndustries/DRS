# Python script to set variables and call ddrescue.

import os, sys, shlex, time, json
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

## Helper Methods
def _PrtDriveParam(head='', pstr=None, color=''):
    """Format input and print header with option"""
    if pstr is not None:
        pstr = "{}{}{}".format(color,pstr,com.color.END) # force string color normal again just incase
        print("{}{} {}{}".format(com.color.HEADER,head,com.color.END,pstr))
    else:
        print("{}{}: None".format(com.color.HEADER,head,com.color.END))

# Mount options for the CIFS server share
RescueMount = ['mount', '-o', 'username=root,password=cw8400,nocase', '//nas/data', '/media/data']

# file system repair after the clone or rescue we need to reset bad blocks and journal files.
NtfsFix = ['ntfsfix', '--clear-bad-sectors', '--clean-dirty']

def lsblk():
    global debug

    if not debug:
        # Block listing with json format so we can parse the device list
        block_list = ['lsblk', '--json', '--noheadings', '--nodeps', '-o', 'name,size,model,serial,fstype']
        try:
            lsblk = Popen(block_list, stdout=PIPE, stderr=PIPE)
            out, err = lsblk.communicate()
        except OSError as _e_:
            print("{}Returned with Error:\n>>>>{}\n>>>>{}\n{}".format(com.color.FAIL,_e_.errno,_e_.strerror,com.color.END))
    
        try:
            decoded = json.loads(out.decode())
        except (ValueError, KeyError, TypeError) as e: # LSBLK is also not in the Linux Subshell for Windows
            print("[{}FAIL{}] lsblk returned the wrong JSON format".format(com.color.FAIL,com.color.END))
            print("{}Returned with:\n>>>{}{}".format(com.color.FAIL,out,com.color.END))
            print(str(e)) # the JSON object must be str, not 'bytes'
            print("Using json dump instead!! {}WARNING{} Falling back in debug mode.".format(com.color.WARNING,com.color.END))
            #decoded = self._loadJsonDump_()
            debug = True
    else: # LSBLK is unsupported on windows use the JSON test data from the Kali Linux VM instead
        decoded = _loadJsonDump_()
    return decoded

def ReadableSize(fstat):
    """Convert file size to MB, KB or Bytes"""
    if (fstat.st_size > 1024 * 1024):
        fsize = math.ceil(fstat.st_size / (1024 * 1024))
        unit = "MB"
    elif (fstat.st_size > 1024):
        fsize = math.ceil(fstat.st_size / 1024)
        unit = "KB"
    else:
        fsize = fstat.st_size
        unit = "B"
    return fsize, unit

def RecoverDirTree(oldPath, newPath, RecoveryOps):
    """Grab directory tree from startpath."""
    for (root,dirs,files) in os.walk(oldPath):
        MkPath = '{}'.format(root.replace(oldPath,newPath,1))
        pathlib.Path(MkPath).mkdir(parents=True, exist_ok=True) # Create Target DIR

        for f in files: # for each file in old path ddrescue to newpath
            OldFile = '{}/{}'.format(root,f)
            NewFile = '{}/{}'.format(root.replace(oldPath,newPath,1),f)
            fsize, unit = ReadableSize(os.stat(os.path.join(root,f)))

            # TODO call DDRescue
            print("{}\t--->\t{}\t{:8d} {:2s}".format(OldFile,NewFile,fsize,unit))
            BLKRecovery(RecoveryOps,OldFile,NewFile)

def BLKRecovery(ops=[], blkdevin='', blkdevout='', mapFile=''):
    """Calls ddrescue with the current configuration"""
    cmdLst = ["ddrescue"] + ops
    cmdLst.append(blkdevin)
    cmdLst.append(blkdevout)
    cmdLst.append(mapFile)
    print(cmdLst)
    rescue = Popen(cmdLst, stderr=PIPE)
    out, err = rescue.communicate()
    print("ERROR: ", err)
    input("Press return/enter to continue...")

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
                         'RecoveryDisk':None, # program gets first block device in list as default
                         'TargetDisk':None,
                         'LogPath':'/var/log',
                         'LogFile':''
                        }
    def Start(self,recType):
        """Start the recovery with the current object settings."""
        mapFile = "{}/{}".format(self._config_['LogPath'],self.GetLogName())
        BLKRecovery(self.GetOps(recType),self._config_['RecoveryDisk'],self._config_['TargetDisk'],mapFile)

    def GetOps(self,recType='full'):
        """Returns recovery options based on type.
        full, noscrape, notrim, clone
        """
        frmtStrLng = "--{}={}"
        frmtStrSrt = "--{}"
        optLst = []

        clusterSize = self._config_['cluster-size']
        skipSize = self._config_['skip-size']
        copyPass = self._config_['cpass']

        for o in self._recoveryType_[recType]:
            optLst += [frmtStrSrt.format(o)]

        if recType == 'clone':
            return [frmtStrLng.format("cluster-size",clusterSize),frmtStrLng.format("cpass","1")] + optLst
        else:
            return [frmtStrLng.format("cluster-size",clusterSize), frmtStrLng.format("skip-size",skipSize),frmtStrLng.format("cpass",copyPass) ] + optLst

    def _DisplayConfigChanges_(self,_newConf_={}):
        """Prints out a side by side view of the configuration settings"""
        self._SettingsTable_.clear_rows() # clean out the table and rebuild a new one with current settings
        for name, value in _newConf_.items():
            self._SettingsTable_.add_row([name,value])
        self._SettingsTable_.sortby = self._SettingsTable_.field_names[0]
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
             UserOptions = self._userqa_()
        return UserOptions

    def _GetConfig(self,name):
        """Gets value by name"""
        return self._config_[name]

    # TODO 1 EXCEPTION on json import, refactor and move to jproc module

    def _GetDevices_(self): # TODO 0 needs refactoring, this is part of Issue #1
        """Get devices from lsblk
        If Win32 OS load lsblkDump.json"""
        print(com.color.BOLD+"\nAttached Storage Devices.\n"+com.color.END)
        UserOptions = self._config_
        _FSignore_ = ['iso9660', 'squashfs']

        # Load data from provider
        BlckDev = lsblk()
        DefVal = False
        for block in BlckDev['blockdevices']:
            if block['fstype'] not in _FSignore_: # Make sure we list only valid drives and are NOT in the Ignore list
                _PrtDriveParam("Drive:  ", block['name'],   com.color.OKGREEN)
                _PrtDriveParam("Size:   ", block['size'],   com.color.WARNING)
                _PrtDriveParam("Serial: ", block['serial'], com.color.BOLD)
                print("") # add a blank line at the end of each group as some values may not print
                if not DefVal:
                    self._config_['RecoveryDisk'] = '/dev/{}'.format(block['name']) # set the default recovery drive to the first one found.
                    DefVal = True