#!/bin/bash

DOWNLOAD_PATH=/mnt/d/PxeTools/ISO
DEVTermIP=192.168.1.24
DEVUser=root
DEVTermSSHPort=22

cd $DOWNLOAD_PATH || echo "Path or directory does not exist /!\\"; exit

rm -v kali-linux-rolling-CI-amd64.iso

ssh $DEVUser@$DEVTermIP -p $DEVTermSSHPort 'service apache2 start; cd ~/repos/DRS; git pull; bash cw_kali_conf.sh'

wget http://$DEVTermIP/kali-linux-rolling-CI-amd64.iso

#TODO Add unpacking and copy for TFTP server location.