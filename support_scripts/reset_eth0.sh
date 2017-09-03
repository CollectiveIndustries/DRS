#!/bin/bash
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
