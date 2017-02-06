#!/usr/bin/env python

# Python script to set variables and call ddrescue.

import ctypes
import os, sys
import shlex
import json
from subprocess import STDOUT,  PIPE, Popen, check_output, CalledProcessError
import time
from datetime import date

from shared import lib

# Vaiable resets
TargetDisk = None
Question = None
RecoverDisk = ''
CustomerName = None
TechInitials = None

# Log file location
RescueLogPath = '/media/data/DDRescue_Logs'

today = date.today()

os.system("clear")

try:
	print "Mounting Storage Server...."
	err = check_output(lib.prog.cifs)
	print lib.color.OKGREEN+"Server Drive Mounted."+lib.color.END
	time.sleep(10)
except CalledProcessError as ERROR:
	print lib.color.FAIL+"ERROR while mounting "+RescueMount[3]+'\nReturned with Error:\n>>>> '+str(ERROR)+lib.color.END
	exit()

# main program loop
while Question is None:
        Question = '' # Reset once we are in the loop
# Clear screen
        os.system("clear")
	print lib.color.BOLD+"\nAttached Storage Devices.\n"+lib.color.END
# Search for disks
#        grep = Popen(['grep','Disk /dev'], stdin=PIPE, stdout=PIPE)
#        fdisk = Popen('fdisk -l'.split(), stdout=grep.stdin)
	lsblk = Popen(lib.prog.lsblk, stdout=PIPE, stderr=PIPE)
	out, err = lsblk.communicate()

	try:
	    decoded = json.loads(out)

	    # Access data
	    for x in decoded['blockdevices']:
		if x['name'] not in lib.ignore.devices: # Make sure we list only valid drives and are NOT in the Ignore list
			print lib.color.HEADER+"Drive:  "+lib.color.OKGREEN+"/dev/"+x['name']+lib.color.END
	 		print lib.color.HEADER+"Size:   "+lib.color.WARNING+x['size']+lib.color.END
			if x['model'] is not None:
				print lib.color.HEADER+"Model:  "+lib.color.END+x['model']
			if x['serial'] is not None:
				print lib.color.HEADER+"Serial: "+lib.color.END+x['serial']
		print "" # add a blank line at the end of each group as some values may not print

	except (ValueError, KeyError, TypeError):
	    print "lsblk returned the wrong JSON format"

# Ask user which drive they want to recover
        RecoverDisk = raw_input('\nDisk to recover (defualt is marked in []): ['+lib.color.OKGREEN+'/dev/sda'+lib.color.END+'] ')
        if RecoverDisk == '':
                RecoverDisk = '/dev/sda' # defualt choice if input is blank.

# Ask user which drive they want to recover
        while ((TargetDisk is None) or (not os.path.exists(TargetDisk))):
		TargetDisk = raw_input(lib.color.FAIL+'Target Drive: '+lib.color.END)

# Search disk for partitions and list them
# fdisk -l /dev/sda | grep "/dev/" | grep -v Disk

        print "\nUsing Disk {}.\n".format(RecoverDisk)
	print "\nThe following numbers may be in decimal, hexadecimal or octal, and may be followed by\na multiplier: s = sectors, k = 1000, Ki = 1024, M = 10^6,  Mi  =  2^20, etc"
	SkipSize = raw_input(lib.color.HEADER+'Skip size?(min,max): '+lib.color.END+'[128s,1M] ')
	if SkipSize == '':
		SkipSize = '128s,1M'
	ClusterSize = raw_input(lib.color.HEADER+'Cluster size?: '+lib.color.END+'[1024] ')
        if ClusterSize == '':
                ClusterSize = '1024'
	while ((CustomerName is None) or CustomerName == ''):
		CustomerName = raw_input(lib.color.FAIL+'Customer Name?: '+lib.color.END+' ')
	while ((TechInitials is None) or TechInitials == ''):
		TechInitials = raw_input(lib.color.FAIL+'Tech Inititals?: '+lib.color.END+' ')

	LogFile = "%s_%s_%s.log" % (CustomerName,today.strftime("%m-%d-%y"),TechInitials)
	LogFile = LogFile.replace(" ","_").replace(",","")

	print "\n"+lib.color.HEADER+"Recovery type:"+lib.color.END+"\nA) Full (runs 3 copy passes, trim, and scrape)\nB) No Scrape (Copy X3, trim)\nC) No Trim (just the copy passes)\nD) Clone (copy pass 1 with a larger read size)\n\nR) Restart\nQ) Quit"
	# Empty suites are considered syntax errors, so intentional fall-throughs
	# should contain 'pass'
	for case in lib.switch(raw_input('Recovery Type []: ')):
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

print "Selected Options."+lib.color.OKBLUE
print "\n".join(str(x) for x in _DD_OPTIONS_).replace("--", "").replace("="," = ")
print lib.color.END+lib.color.WARNING+"Executing ddrescue."+lib.color.END

os.system("clear")

# fork the subprocess here
r, w = os.pipe() # these are file descriptors, not file objects

pid = os.fork()
if pid:
    # we are the parent
    os.close(w) # use os.close() to close a file descriptor
    try:
	print lib.color.OKGREEN+'ddrescue '+RecoverDisk+' '+TargetDisk+' '+LogFile+lib.color.END
	rescue = Popen(['ddrescue']+_DD_OPTIONS_+[RecoverDisk,TargetDisk,RescueLogPath+"/"+LogFile],  stderr=PIPE)
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
