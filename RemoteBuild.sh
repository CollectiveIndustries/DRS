#!/bin/bash

DOWNLOAD_PATH=ISO-Storage
TMP_Mount=iso-mntpoint
ISO_NAME=Kali-CI-$(date +"%m-%d-%Y").iso

DEVTermIP=192.168.1.24
DEVUser=root
DEVTermSSHPort=22

# DO NOT Change this unless your PXE Server is NOT located in this location!!!!
PXE_Boot_Root=/media

cd $PXE_Boot_Root/$DOWNLOAD_PATH || echo "Path or directory does not exist /!\\"; exit

ssh $DEVUser@$DEVTermIP -p $DEVTermSSHPort 'service apache2 start; cd ~/repos/DRS; git pull; bash cw_kali_conf.sh'

wget -O $ISO_NAME http://$DEVTermIP/kali-linux-rolling-CI-amd64.iso

mount -o loop $ISO_NAME $PXE_Boot_Root/$TMP_Mount

cp $PXE_Boot_Root/$TMP_Mount/live/filesystem.squashfs $PXE_Boot_Root/SquashFS/kali-CI.squashfs


# DirectoryTree = {Apache-webshare,TFTP-Boot,FTP-share,SMB-share,NFS-Config,ISO-Storage,SquashFS}

# TFTP-Root
#		|
#		|
#	[SquashFS]
#			|
#		(distro.squashfs)