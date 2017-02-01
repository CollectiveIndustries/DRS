#!/usr/bin/env python3

# Python script to set variables and call rsync.

import ctypes
import os, sys
import shlex
import json
from subprocess import PIPE, Popen, check_output
import time
from datetime import date

# Vaiable resets
TargetPart = None
Question = None
BackupDisk = ''
CustomerName = None
TechName = None

class prog:
	lsblk = ['lsblk', '--json', '--noheadings', '-o', 'name,size,model,serial,fstype,label']
	rsync = ['rsync', '--recursive', '--compress-level=9', '--human-readable', '--progress', '--no-perms', '--no-owner', '--no-group', '--no-times', '--ignore-existing', '--exclude-from=/etc/rsync_exclude.conf']
	cp = ['cp', '/media/cw/Drew/Live_USB/scripts/rsync_exclude.conf', '/etc/rsync_exclude.conf']
	ntfs = ['lowntfs-3g', '-o', 'windows_names,ignore_case']
	cifs = ['mount.cifs', '-o', 'username=root,password=cw8400', '//nas/data', '/media/data']

# class container for Ignore lists
# TODO set up regex for these to avoid adding loop0 loop1...loopX

class ignore:
	filesystems = ['iso9660', 'squashfs', 'crypto_LUKS', None, 'swap']
	devices = ['sr0', 'sr1', 'loop0']

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

print("Reading exclude list.....")

cp = Popen(prog.cp, stdout=PIPE, stderr=PIPE)
cout, cerr = cp.communicate()

print(color.OKGREEN+"[DONE]"+color.END)

# main program loop
while Question is None:
# Clear screen
	os.system("clear")
	print(color.BOLD+"\nAttached Storage Devices.\n"+color.END)

# Search for disks
	lsblk = Popen(prog.lsblk, stdout=PIPE, stderr=PIPE)
	out, err = lsblk.communicate()
#	print(out)

	try:
		decoded = json.loads(out.decode("utf-8"))


	# Access data
		for x in decoded['blockdevices']:
			if x['name'] not in ignore.devices: # Display valid disks with a SN
				print(color.HEADER+"Drive:  "+color.OKGREEN+"/dev/"+x['name']+color.END)
				print(color.HEADER+"Size:   "+color.WARNING+x['size']+color.END)
				if x['model'] is not None:
					print(color.HEADER+"Model:  "+color.END+x['model'])
				if x['serial'] is not None:
					print(color.HEADER+"Serial: "+color.END+x['serial'])
					print("")
				for c in x['children']:
					if c['fstype'] not in ignore.filesystems:
						print('\t'+color.UNDERLINE+'Partition:'+color.END)
						print("\t"+color.HEADER+"Name:  "+color.OKGREEN+"/dev/"+c['name']+color.END)
						if c['label'] is not None:
							print("\t"+color.HEADER+"Label: "+color.END+c['label'])

						if c['fstype'] is not None:
							print("\t"+color.HEADER+"Type:  "+color.END+c['fstype'])
						else:
							print("\t"+color.HEADER+"Type:  "+color.FAIL+"UNKNOWN"+color.END)

						if c['size'] is not None:
							print("\t"+color.HEADER+"Size:  "+color.WARNING+c['size']+color.END)
						else:
							print("\t"+color.HEADER+"Size:  "+color.FAIL+"UNKNOWN"+color.END)

						print("")
			print("") # add a blank line at the end of each group as some values may not print

	except (ValueError, KeyError, TypeError):
		print(color.FAIL+"There was a problem parsing the JavaScript Object Notation (JSON)"+color.END)
		print(ValueError.msg)
		exit(1)

# Ask user which drive they want to recover
	print("All default options are marked with []")
	BackupDisk = input('\nPartition to backup: ['+color.OKGREEN+'/dev/sda1'+color.END+'] ')
	if BackupDisk == '':
		BackupDisk = '/dev/sda1' # defualt choice if input is blank.

	print(color.HEADER+"Choose target type:"+color.END)
	print("A) Server. Cifs share //nas/data")
	print("B) Local Partition")
	print("\nR) Rescan Device list")
	for case in switch(input('Target Type [A) Server]: ')):
		print("\n") # pad down a few lines then print selected options.
		if case('B'): pass
		if case('b'):
			while ((TargetPart is None) or (TargetPart == '')):
				TargetPart = input(color.FAIL+"Target partition: "+color.END)
			MountCommand = prog.ntfs + [TargetPart, '/media/data']
			DestFolder = 'Data/' # local backups to systems need to go into the Data folder
			Question = 'B'
			break
		if case('R'): pass
		if case('r'): # Fall through to the end of the loop and rescan targets
			Question = None
			break
		if case('A'): pass # only necessary if the rest of the suite is empty
		if case('a'): pass # Backup data to cifs share by defualt
		if case(): # Default option
			print("Target: Server (//nas/data/)")
			MountCommand = prog.cifs
			Question = 'A'
			while ((CustomerName is None) or (CustomerName == '')):
				CustomerName = input(color.FAIL+"Customer name: "+color.END)

			while ((TechName is None) or (TechName == '')):
				TechName = input(color.FAIL+"Tech Initials: "+color.END)

			DestFolder = CustomerName+' '+today.strftime("%m-%d-%y")+' '+TechName+'/'
			# Support for "Lastname, Firstname DATE TECH" as the folder name
			break


# Mount the filesystem
DestMount = Popen(MountCommand, stdout=PIPE, stderr=PIPE)
Dout, Derr = DestMount.communicate()

SourceMount = Popen(prog.ntfs+[BackupDisk, '/mnt'], stdout=PIPE, stderr=PIPE)
Sout, Serr = SourceMount.communicate()

# Start the sync

start_time = time.time()

Sync = Popen(prog.rsync+['/mnt/','/media/data/'+DestFolder], stderr=PIPE)
Sync.communicate() # Wait for the process to finish

# Silently kill error output, let the normal output go to the screen

end_time = time.time()

hours, rem = divmod(end_time-start_time, 3600)
minutes, seconds = divmod(rem, 60)

print(color.OKGREEN+"Backup finished in:"+color.END)
print("{:0>2} Hour(s) {:0>2} Minutes {:05.2f} Seconds".format(int(hours),int(minutes),seconds))

# End the program
