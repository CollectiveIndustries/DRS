#!/usr/bin/env python

# Python script to set variables and call ddrescue.

import ctypes
import os, sys
import shlex
from subprocess import PIPE, Popen

# Vaiable resets
TargetDisk = None
Question = 'r'
RecoverDisk = ''

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

# main program loop
while Question.lower() == 'r':
        Question = '' # Reset once we are in the loop
# Clear screen
        os.system("clear")

# Search for disks
#        grep = Popen(['grep','Disk /dev'], stdin=PIPE, stdout=PIPE)
#        fdisk = Popen('fdisk -l'.split(), stdout=grep.stdin)
	lsblk = Popen(['lsblk', '--pairs', '--output','NAME,SIZE,LABEL,MODEL,SERIAL'])
        disks = lsblk.communicate()[0]
#        fdisk.wait()
        print 'Disk Selection\n\n{}'.format(disks)

# Ask user which drive they want to recover
        RecoverDisk = raw_input('Disk to recover (defualt is marked in []): [/dev/sda] ')
        if RecoverDisk == '':
                RecoverDisk = '/dev/sda' # defualt choice if input is blank.

# Ask user which drive they want to recover
        while ((TargetDisk is None) or (not os.path.exists(TargetDisk))):
		TargetDisk = raw_input('Target Drive: [] ')

# Search disk for partitions and list them
# fdisk -l /dev/sda | grep "/dev/" | grep -v Disk

        print "\nUsing Disk {}.\n".format(RecoverDisk)
	SkipSize = raw_input('Skip size?( ): [128s] ')
	if SkipSize == '':
		SkipSize = '128s'
	print "\nRecovery type:\nA) Full (runs 3 copy passes, trim, and scrape)\nB) No Scrape (Copy X3, trim)\nC) No Trim (just the copy passes)\nD) Clone (copy pass 1 with a larger read size)\n\nR) Restart\nQ) Quit"
	# Empty suites are considered syntax errors, so intentional fall-throughs
	# should contain 'pass'
	for case in switch(raw_input('Recovery Type []: ')):
		print "\n\n" # padd down a few lines then print selected options.
		if case('A'): pass # only necessary if the rest of the suite is empty
		if case('a'): # Full recovery
			#
			_DD_OPTIONS_ = ['--skip-size '+SkipSize, '--reopen-on-error', '--direct', '--force', '--verbose']
			print "Full Recovery selected.\n{} Skipsize\nDirect write access: TRUE\nreopen drive on error: TRUE\n/!\\WARNING/!\\ Force overwrite: TRUE\nSCRAPE: TRUE\nTrim: TRUE\nCopy Pass: 1,2,3"
			break
	    	if case('B'): pass
		if case('b'): # No Scrape
			#
			_DD_OPTIONS_ = ['--skip-size '+SkipSize, '--reopen-on-error', '--direct', '--force', '--verbose', '--no-scrape']
			print "No Scrape Recovery selected.\n{} Skipsize\nDirect write access: TRUE\nreopen drive on error: TRUE\n/!\\WARNING/!\\ Force overwrite: TRUE\nSCRAPE: FALSE\nTrim: TRUE\nCopy Pass: 1,2,3"
	        	break
	    	if case('C'): pass
	    	if case('c'): # No trim
			#
			_DD_OPTIONS_ = ['--skip-size '+SkipSize, '--reopen-on-error', '--direct', '--force', '--verbose', '--no-scrape', '--no-trim']
			print "Full Recovery selected.\n{} Skipsize\nDirect write access: TRUE\nreopen drive on error: TRUE\n/!\\WARNING/!\\ Force overwrite: TRUE\nSCRAPE: FALSE\nTrim: FALSE\nCopy Pass: 1,2,3"
	        	break
		if case('D'): pass
		if case('d'): # Single forward copy (large block size) good drive clone
			#
			_DD_OPTIONS_ = ['--cpass=1', '--cluster-size=1024', '--direct', '--force', '--verbose', '--no-trim', '--no-scrape']
			print "Full Recovery selected.\n128 sector Skipsize (default)\nDirect write access: TRUE\nreopen drive on error: TRUE\n/!\\WARNING/!\\ Force overwrite: TRUE\nSCRAPE: FALSE\nTrim: FALSE\nCopy Pass: 1\nCopy Cluster Size: 1024 Sectors"
			break
		if case('r'): pass
		if case('R'):
			Question = 'r' # Restart the prompts
		if case('q'): pass
		if case('Q'):
			print "Program Terminated"
			exit(0) #normal program termination
	    	if case(): # default
	        	print "Please make a valid selection."
			Question = 'r' # restart the prompts
