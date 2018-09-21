#!/bin/bash


## This needs to to support multiple adapters with an input parameter from the shell
## maybe just move this entire thing into the python code cant remmber why its here tbh

clear
ifdown eth0
echo " "
echo " ## iface eth0 down ## "
echo " "
ifup eth0
echo " "
echo " ## iface eth0 up ## "
echo " "
ifconfig eth0
