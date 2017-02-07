#!/usr/bin/env python3

# Python script to find and mount a filesystem and then rescue data at the file system level.
# If this fails to mount the disk we may need to image the drive.

import ctypes
import os, sys
import shlex
import json
from subprocess import PIPE, Popen, check_output
import time
from datetime import date

from shared import lib

# Vaiable resets
TargetPart = None
Question = None
BackupDisk = ''
CustomerName = None
TechName = None

today = date.today()

print("Reading exclude list.....")

cp = Popen(lib.prog.cp, stdout=PIPE, stderr=PIPE)
cout, cerr = cp.communicate()

print(lib.color.OKGREEN+"[DONE]"+lib.color.END)

# main program loop
while Question is None:
# Clear screen
	os.system("clear")
	print(lib.color.BOLD+"\nAttached Storage Devices.\n"+lib.color.END)

# Search for disks
	lsblk = Popen(lib.prog.lsblk, stdout=PIPE, stderr=PIPE)
	out, err = lsblk.communicate()
#	print(out)

	try:
		decoded = json.loads(out.decode("utf-8"))


	# Access data
		for x in decoded['blockdevices']:
			if x['name'] not in lib.ignore.devices: # Display valid disks with a SN
				print(lib.color.HEADER+"Drive:  "+lib.color.OKGREEN+"/dev/"+x['name']+lib.color.END)
				print(lib.color.HEADER+"Size:   "+lib.color.WARNING+x['size']+lib.color.END)
				if x['model'] is not None:
					print(lib.color.HEADER+"Model:  "+lib.color.END+x['model'])
				if x['serial'] is not None:
					print(lib.color.HEADER+"Serial: "+lib.color.END+x['serial'])
					print("")
				for c in x['children']:
					if c['fstype'] not in lib.ignore.filesystems:
						print('\t'+lib.color.UNDERLINE+'Partition:'+lib.color.END)
						print("\t"+lib.color.HEADER+"Name:  "+lib.color.OKGREEN+"/dev/"+c['name']+lib.color.END)
						if c['label'] is not None:
							print("\t"+lib.color.HEADER+"Label: "+lib.color.END+c['label'])

						if c['fstype'] is not None:
							print("\t"+lib.color.HEADER+"Type:  "+lib.color.END+c['fstype'])
						else:
							print("\t"+lib.color.HEADER+"Type:  "+lib.color.FAIL+"UNKNOWN"+lib.color.END)

						if c['size'] is not None:
							print("\t"+lib.color.HEADER+"Size:  "+lib.color.WARNING+c['size']+lib.color.END)
						else:
							print("\t"+lib.color.HEADER+"Size:  "+lib.color.FAIL+"UNKNOWN"+lib.color.END)

						print("")
			print("") # add a blank line at the end of each group as some values may not print

	except (ValueError, KeyError, TypeError):
		print(lib.color.FAIL+"There was a problem parsing the JavaScript Object Notation (JSON)"+lib.color.END)
		print(ValueError.msg)
		exit(1)

# Ask user which drive they want to recover
	print("All default options are marked with []")
	BackupDisk = input('\nPartition to backup: ['+lib.color.OKGREEN+'/dev/sda1'+lib.color.END+'] ')
	if BackupDisk == '':
		BackupDisk = '/dev/sda1' # defualt choice if input is blank.

	print(lib.color.HEADER+"Choose target type:"+lib.color.END)
	print("A) Server. Cifs share //nas/data")
	print("B) Local Partition")
	print("\nR) Rescan Device list")
	for case in lib.switch(input('Target Type [A) Server]: ')):
		print("\n") # pad down a few lines then print selected options.
		if case('B'): pass
		if case('b'):
			while ((TargetPart is None) or (TargetPart == '')):
				TargetPart = input(lib.color.FAIL+"Target partition: "+lib.color.END)
			MountCommand = lib.prog.ntfs + [TargetPart, '/media/data']

			# unmount filesystem before trying to mount it
			Umount = Popen(lib.prog.umount + [TargetPart], stdout=PIPE, stderr=PIPE)
			Umount.communicate()

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
			MountCommand = lib.prog.cifs
			Question = 'A'
			while ((CustomerName is None) or (CustomerName == '')):
				CustomerName = input(lib.color.FAIL+"Customer name: "+lib.color.END)

			while ((TechName is None) or (TechName == '')):
				TechName = input(lib.color.FAIL+"Tech Initials: "+lib.color.END)

			DestFolder = CustomerName+' '+today.strftime("%m-%d-%y")+' '+TechName+'/'
			# Support for "Lastname, Firstname DATE TECH" as the folder name
			break


# Unmount filesystems in preperation of mounting them.
UmountBack = Popen(lib.prog.umount+[BackupDisk], stdout=PIPE, stderr=PIPE)
UmountBack.communicate()

# Mount the filesystem
DestMount = Popen(MountCommand, stdout=PIPE, stderr=PIPE)
Dout, Derr = DestMount.communicate()

SourceMount = Popen(lib.prog.ntfs+[BackupDisk, '/mnt'], stdout=PIPE, stderr=PIPE)
Sout, Serr = SourceMount.communicate()

# Start the sync

start_time = time.time()

Sync = Popen(lib.prog.rsync+['/mnt/','/media/data/'+DestFolder], stderr=PIPE)
Sync.communicate() # Wait for the process to finish

# Silently kill error output, let the normal output go to the screen

end_time = time.time()

hours, rem = divmod(end_time-start_time, 3600)
minutes, seconds = divmod(rem, 60)

print(lib.color.OKGREEN+"Backup finished in:"+lib.color.END)
print("{:0>2} Hour(s) {:0>2} Minutes {:05.2f} Seconds".format(int(hours),int(minutes),seconds))

# End the program
