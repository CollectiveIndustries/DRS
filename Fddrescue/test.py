#!/usr/bin/env python

from subprocess import STDOUT,  PIPE, Popen, check_output, CalledProcessError
from module import disk,com

def GetTree(path='/mnt'):
        disk.prog.find[1]=path
        find = Popen(disk.prog.find, stdout=PIPE, stderr=PIPE)
        out, err = find.communicate()
	return([s.strip() for s in out.splitlines()])

def SetTree(path):
	disk.prog.mkdir[2] = path
	mkdir = Popen(disk.prog.mkdir, stdout=PIPE, stderr=PIPE)
	out, err = mkdir.communicate()

print(GetTree('/etc'))
