#!/bin/bash

cd /mnt/d/ISO || exit

rm -v kali-linux-rolling-CI-amd64.iso

ssh root@192.168.1.24 'service apache2 start; cd ~/repos/DRS; git pull; bash cw_kali_conf.sh'

wget http://192.168.1.24/kali-linux-rolling-CI-amd64.iso