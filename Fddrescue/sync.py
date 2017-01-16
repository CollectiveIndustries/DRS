#!/usr/bin/env python

# Python script to set variables and call ddrescue.

import ctypes
import os, sys
import shlex
import json
from subprocess import PIPE, Popen
import time
from datetime import date

# Vaiable resets
TargetDisk = None
Question = None
RecoverDisk = ''
CustomerName = None

BackupServer = '//nas/data'
MediaLocation = '/media/data/'

LocalMount = ['lowntfs-3g', '-o', 'windows_names,ignore_case']
NasMount = ['mount.cifs', BackupServer, '-o', 'username=root,password=cw8400', MediaLocation]

# get a list of block devices
block_list = ['lsblk', '--json', '--noheadings', '-o', 'name,size,model,serial,fstype']
Rsync = ['rsync', '--recursive', '--compress-level=9', '--human-readable', '--progress', '--list-only', '--exclude-from=/etc/rsync_exclude.conf']

# This class provides the functionality we want. You only need to look at
# this if you want to know how this works. It only needs to be defined
# once, no need to muck around with its internals.
# Located at http://code.activestate.com/recipes/410692/
class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args:
            self.fall = True
            return True
        else:
            return False


# Text output color definitions
class color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

today = date.today()

# main program loop
while Question is None:
# Clear screen
        os.system("clear")
	print color.BOLD+"\nAttached Storage Devices.\n"+color.END

# Search for disks
	lsblk = Popen(block_list, stdout=PIPE, stderr=PIPE)
	out, err = lsblk.communicate()

	try:
	    decoded = json.loads(out)

	    # Access data
	    for x in decoded['blockdevices']:
		if x['fstype'] != 'iso960': # Display valid disks with a SN
			print color.HEADER+"Drive:  "+color.OKGREEN+"/dev/"+x['name']+color.END
	 		print color.HEADER+"Size:   "+color.WARNING+x['size']+color.END
			if x['model'] is not None:
				print color.HEADER+"Model:  "+color.END+x['model']
			if x['serial'] is not None:
				print color.HEADER+"Serial: "+color.END+x['serial']
			for c in x['children']:
				print "\t"+color.HEADER+"Partition: "+color.OKGREEN+"/dev/"+c['name']+color.END
				if c['fstype'] is not None:
					print "\t"+color.HEADER+"Partition Type: "+color.OKGREEN+c['fstype']+color.END
				else:
					print "\t"+color.HEADER+"Partition Type: "+color.FAIL+"UNKNOWN"+color.END
				if c['size'] is not None:
					print "\t"+color.HEADER+"Partition Size: "+color.OKGREEN+c['size']+color.END
				else:
					print"\t"+color.HEADER+"Partition Size: "+color.FAIL+"UNKNOWN"+color.END
				print ""
		print "" # add a blank line at the end of each group as some values may not print

	except (ValueError, KeyError, TypeError):
	    print "lsblk returned the wrong JSON format"

# Ask user which drive they want to recover
	print "All default options are marked with []"
        RecoverDisk = raw_input('\nPartition to backup: ['+color.OKGREEN+'/dev/sda1'+color.END+'] ')
        if RecoverDisk == '':
                RecoverDisk = '/dev/sda1' # defualt choice if input is blank.
	print color.HEADER+"Choose target type:"+.color.END
        for case in switch(raw_input('Target Type [A) Server]: ')):
                print "\n\n" # pad down a few lines then print selected options.
                if case('A'): pass # only necessary if the rest of the suite is empty
                if case('a'): # Full recovery
                        #
                        print "Target: Server (//nas/data/)"
			MountOptions = ['//nas/data', '/media/data']
                        Question = ''
                        break

	break

