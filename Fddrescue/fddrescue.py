#!/usr/bin/env python

# Python script to find and mount a filesystem and then rescue data at the file system level.
# If this fails to mount the disk we may need to image the drive.

import ctypes
import os, sys
import shlex
from subprocess import PIPE, Popen

# Variable resets.
TargetDisk = None
RecoverPart = 'r'
RecoverDisk = None

# mount binding for python
def mount(source, target, fs, options=''):
  ret = ctypes.CDLL('libc.so.6', use_errno=True).mount(source, target, fs, 0, options)
  if ret < 0:
    errno = ctypes.get_errno()
    raise RuntimeError("Error mounting {} ({}) on {} with options '{}': {}".
     format(source, fs, target, options, os.strerror(errno)))

while RecoverPart.lower() == 'r':
	RecoverPart = '' # Reset once we are in the loop
# Clear screen
	os.system("clear")

# Search for disks
	grep = Popen(['grep','Disk /dev'], stdin=PIPE, stdout=PIPE)
	fdisk = Popen('fdisk -l'.split(), stdout=grep.stdin)
	disks = grep.communicate()[0]
	fdisk.wait()
	print '{}'.format(disks)

# Ask user which drive they want to recover
	RecoverDisk = raw_input('Disk to recover (defualt is marked in []): [/dev/sda] ')
	if RecoverDisk == '':
		RecoverDisk = '/dev/sda' # defualt choice if input is blank.

# Search disk for partitions and list them
# fdisk -l /dev/sda | grep "/dev/" | grep -v Disk

	print "\nUsing Disk {}.\n\nListing found Partitions:\n".format(RecoverDisk)

# Grab partitions disk
	p1 = Popen(['fdisk','-l', RecoverDisk], stdout=PIPE)
	p2 = Popen(['grep','/dev/'], stdin=p1.stdout, stdout=PIPE)
	p1.stdout.close()
	p3 = Popen(['grep','-v','Disk'], stdin=p2.stdout,stdout=PIPE)
	p2.stdout.close()

	Partitions = p3.communicate()[0]
	print '{}'.format(Partitions)

	while RecoverPart == '':
		RecoverPart = raw_input('Partition to recover (cannot be left blank R to return to disk selection, Q to Quit): ')
		if RecoverPart.lower() == 'r':
			break
		if RecoverPart.lower() == 'q':
			sys.exit(0)
