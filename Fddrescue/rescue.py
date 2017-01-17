#!/usr/bin/env python

# Python script to set variables and call ddrescue.

import ctypes
import os, sys
import shlex
import json
from subprocess import STDOUT,  PIPE, Popen, check_output, CalledProcessError
import time
from datetime import date

# Vaiable resets
TargetDisk = None
Question = None
RecoverDisk = ''
CustomerName = None
TechInitials = None


RescueMount = ['mount.cifs', '-o', 'username=root,password=cw8400,nocase', '//nas/data','/media/data']
block_list = ['lsblk', '--json', '--noheadings', '--nodeps', '-o', 'name,size,model,serial,fstype']

RescueLogPath = '/media/data/DDRescue_Logs'

# File Systems we dont need to list, genrelly these are internal or Live file systems from the USB
FSIgnore = ['iso9660', 'squashfs']


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

os.system("clear")

try:
	print "Mounting Storage Server...."
	err = check_output(RescueMount)
	print color.OKGREEN+"Server Drive Mounted."+color.END
	time.sleep(10)
except CalledProcessError as ERROR:
	print color.FAIL+"ERROR while mounting "+RescueMount[3]+'\nReturned with Error:\n>>>> '+str(ERROR)+color.END
	exit()

# main program loop
while Question is None:
        Question = '' # Reset once we are in the loop
# Clear screen
        os.system("clear")
	print color.BOLD+"\nAttached Storage Devices.\n"+color.END
# Search for disks
#        grep = Popen(['grep','Disk /dev'], stdin=PIPE, stdout=PIPE)
#        fdisk = Popen('fdisk -l'.split(), stdout=grep.stdin)
	lsblk = Popen(block_list, stdout=PIPE, stderr=PIPE)
	out, err = lsblk.communicate()

	try:
	    decoded = json.loads(out)

	    # Access data
	    for x in decoded['blockdevices']:
		if x['fstype'] not in FSIgnore: # Make sure we list only valid drives and are NOT in the Ignore list
			print color.HEADER+"Drive:  "+color.OKGREEN+"/dev/"+x['name']+color.END
	 		print color.HEADER+"Size:   "+color.WARNING+x['size']+color.END
			if x['model'] is not None:
				print color.HEADER+"Model:  "+color.END+x['model']
			if x['serial'] is not None:
				print color.HEADER+"Serial: "+color.END+x['serial']
		print "" # add a blank line at the end of each group as some values may not print

	except (ValueError, KeyError, TypeError):
	    print "lsblk returned the wrong JSON format"

# Ask user which drive they want to recover
        RecoverDisk = raw_input('\nDisk to recover (defualt is marked in []): ['+color.OKGREEN+'/dev/sda'+color.END+'] ')
        if RecoverDisk == '':
                RecoverDisk = '/dev/sda' # defualt choice if input is blank.

# Ask user which drive they want to recover
        while ((TargetDisk is None) or (not os.path.exists(TargetDisk))):
		TargetDisk = raw_input(color.FAIL+'Target Drive: '+color.END)

# Search disk for partitions and list them
# fdisk -l /dev/sda | grep "/dev/" | grep -v Disk

        print "\nUsing Disk {}.\n".format(RecoverDisk)
	print "\nThe following numbers may be in decimal, hexadecimal or octal, and may be followed by\na multiplier: s = sectors, k = 1000, Ki = 1024, M = 10^6,  Mi  =  2^20, etc"
	SkipSize = raw_input(color.HEADER+'Skip size?(min,max): '+color.END+'[128s,1M] ')
	if SkipSize == '':
		SkipSize = '128s,1M'
	ClusterSize = raw_input(color.HEADER+'Cluster size?: '+color.END+'[1024] ')
        if ClusterSize == '':
                ClusterSize = '1024'
	while ((CustomerName is None) or CustomerName == ''):
		CustomerName = raw_input(color.FAIL+'Customer Name?: '+color.END+' ')
	while ((TechInitials is None) or TechInitials == ''):
		TechInitials = raw_input(color.FAIL+'Tech Inititals?: '+color.END+' ')

	LogFile = "%s_%s_%s.log" % (CustomerName,today.strftime("%m-%d-%y"),TechInitials)
	LogFile = LogFile.replace(" ","_").replace(",","")

	print "\n"+color.HEADER+"Recovery type:"+color.END+"\nA) Full (runs 3 copy passes, trim, and scrape)\nB) No Scrape (Copy X3, trim)\nC) No Trim (just the copy passes)\nD) Clone (copy pass 1 with a larger read size)\n\nR) Restart\nQ) Quit"
	# Empty suites are considered syntax errors, so intentional fall-throughs
	# should contain 'pass'
	for case in switch(raw_input('Recovery Type []: ')):
		print "\n\n" # padd down a few lines then print selected options.
		if case('A'): pass # only necessary if the rest of the suite is empty
		if case('a'): # Full recovery
			#
			_DD_OPTIONS_ = ['--cluster-size='+ClusterSize, '--skip-size='+SkipSize, '--reopen-on-error', '--idirect', '--odirect', '--force', '--verbose']
			print "Full Recovery selected."
			Question = ''
			break
	    	if case('B'): pass
		if case('b'): # No Scrape
			#
			_DD_OPTIONS_ = ['--cluster-size='+ClusterSize, '--skip-size='+SkipSize, '--reopen-on-error', '--idirect', '--odirect', '--force', '--verbose', '--no-scrape']
			print "No Scrape Recovery selected."
			Question = ''
	        	break
	    	if case('C'): pass
	    	if case('c'): # No trim
			#
			_DD_OPTIONS_ = ['--cluster-size='+ClusterSize, '--skip-size='+SkipSize, '--reopen-on-error', '--idirect', '--odirect', '--force', '--verbose', '--no-scrape', '--no-trim']
			print "Full 3 pass clone selected."
			Question = ''
	        	break
		if case('D'): pass
		if case('d'): # Single forward copy (large block size) good drive clone
			#
			_DD_OPTIONS_ = ['--cluster-size='+ClusterSize, '--cpass=1', '--idirect', '--odirect', '--force', '--verbose', '--no-trim', '--no-scrape']
			print "Single pass Clone selected."
			Question = ''
			break
		if case('r'): pass
		if case('R'): break # user selected R/r for Rerun

		if case('q'): pass
		if case('Q'):
			print "Program Terminated"
			exit(0) #normal program termination
	    	if case(): # default
	        	print "Please make a valid selection."
			# restart the prompts

print "Selected Options."+color.OKBLUE
print "\n".join(str(x) for x in _DD_OPTIONS_).replace("--", "").replace("="," = ")
print color.END+color.WARNING+"Executing ddrescue."+color.END

os.system("clear")

# fork the subprocess here
r, w = os.pipe() # these are file descriptors, not file objects

pid = os.fork()
if pid:
    # we are the parent
    os.close(w) # use os.close() to close a file descriptor
    try:
	print color.OKGREEN+'ddrescue '+RecoverDisk+' '+TargetDisk+' '+LogFile+color.END
	rescue = Popen(['ddrescue']+_DD_OPTIONS_+[RecoverDisk,TargetDisk,RescueLogPath+"/"+LogFile],  stderr=PIPE)
	out, err = rescue.communicate()
	print out
	print color.FAIL+err+color.END

    except:
	print "Error trying to call rescue"

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
