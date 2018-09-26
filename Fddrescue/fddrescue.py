#!/usr/bin/env python

# Python script to find and mount a filesystem and then rescue data at the file system level.
# If this fails to mount the disk we may need to image the drive.

# TODO clean up import list
import os, sys
import time
from lib import com, disk

# Variable resets.
TargetDisk = None
RecoverPart = 'r'
RecoverDisk = None

RecoverList = ['Movies','Games','Music']

# TODO Start working on FDDRescue module.
# finish workflow
# set up file recovery task

tmpFile = open("/tmp/rescue.sh", "w+")

#add the bash Shabang before we add all the files to the recovery script
tmpFile.write("#!/bin/bash\n")

while RecoverPart.lower() == 'r':
	RecoverPart = '' # Reset once we are in the loop
# Clear screen
	os.system("clear")

	disk.listFileSystems() # List all known file systems and block devices

# Ask user which drive they want to recover
#	RecoverDisk = raw_input('Disk to recover (defualt is marked in []): [{}/dev/sda{}] '.format(com.color.OKGREEN,com.color.END))
#	if RecoverDisk == '':
#		RecoverDisk = '/dev/sda' # defualt choice if input is blank.

	while RecoverPart == '':
		RecoverPart = raw_input('Partition to recover (cannot be left blank R to return to disk selection, Q to Quit): ')
		if RecoverPart.lower() == 'r':
			break
		if RecoverPart.lower() == 'q':
			sys.exit(0)

	while TargetDisk == None:
		TargetDisk = raw_input('Target Location: [{}/media/data{}]'.format(com.color.OKGREEN,com.color.END))
		if TargetDisk == '':
			TargetDisk = '/media/data/'

	print("Mounting [{}{}{}] on [{}/mnt{}]".format(com.color.OKGREEN,RecoverPart,com.color.END,com.color.OKGREEN,com.color.END))
	# Mount Recovery Part Read ONLY
	print("Building Recovery script")
	disk.mount(RecoverPart,'/mnt','ntfs',0)
	time.sleep(5)
	for item in RecoverList:
		for OldPath in disk.GetTree('/mnt/'+item):
			NewPath = OldPath.replace('/mnt','/media/root/4a6c65b0-7cf1-4139-b210-d52b562cae24/recovered',1)
			disk.SetTree(NewPath)
#			print("{}mkdir -p {}{}".format(com.color.OKGREEN,NewPath,com.color.END))
			for file in disk.GetFiles(OldPath):
				file = file.split('/')[-1]
#				print("Recovering {}{}{} into {}{}{}".format(com.color.OKGREEN,file,com.color.END,com.color.WARNING,NewPath,com.color.END))
				tmpFile.write(disk.Rescue("{}/{}".format(OldPath,file), "{}/{}".format(NewPath,file)))
				tmpFile.write("\n")
tmpFile.close()
