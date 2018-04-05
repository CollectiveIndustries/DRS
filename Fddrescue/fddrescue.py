#!/usr/bin/env python

# Python script to find and mount a filesystem and then rescue data at the file system level.
# If this fails to mount the disk we may need to image the drive.

import os, sys
import shlex
from subprocess import PIPE, Popen
from module import com, disk

# Variable resets.
TargetDisk = None
RecoverPart = 'r'
RecoverDisk = None

while RecoverPart.lower() == 'r':
	RecoverPart = '' # Reset once we are in the loop
# Clear screen
	os.system("clear")

	disk.listFileSystems() # List all known file systems and block devices

# Ask user which drive they want to recover
	RecoverDisk = raw_input('Disk to recover (defualt is marked in []): [{}/dev/sda{}] '.format(com.color.OKGREEN,com.color.END))
	if RecoverDisk == '':
		RecoverDisk = '/dev/sda' # defualt choice if input is blank.

	while RecoverPart == '':
		RecoverPart = raw_input('Partition to recover (cannot be left blank R to return to disk selection, Q to Quit): ')
		if RecoverPart.lower() == 'r':
			break
		if RecoverPart.lower() == 'q':
			sys.exit(0)
