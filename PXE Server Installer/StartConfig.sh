#!/bin/bash


if [ "$1" = "--win10-install" ]
then
	cat << EOF > start.cmd
	net use I:\ //192.168.1.210/microsoft-installers/lgts-win10
	I:\setup.exe
	EOF
elif ["$1" = "--win7-install"]
then
	cat << EOF > start.cmd
	net use I:\ //192.168.1.210/microsoft-installers/win7pr0
	I:\setup.exe
	EOF
elif [ "$1" = "--live-boot"]
then
	cat << EOF > start.cmd
	cmd.exe
	pause
fi