#!/bin/bash

# Set Common Config variables here
LAN_ADDY=192.168.0.0/24
DESKTOP_WALLPAPER=/media/cw/Live_USB/background/Background.png
USB_SPLASH=/media/cw/Live_USB/background/cwsplash.png
ICON_CACHE=/usr/share/icons/cw

# clear the work space and start configuration
clear
apt-get autoclean --force-yes -y
apt-get autoremove --force-yes -y
proxychains apt-get update
proxychains apt-get dist-upgrade --force-yes -y

# use the proxy tunnel or regular git clone place the resulting repository in the Home SOURCE Directory.
cd ~/SOURCE

proxychains git clone git://git.kali.org/live-build-config.git
#git clone git://git.kali.org/live-build-config.git


# change to the working directory so we can run the base distro config scripts
cd live-build-config

# make the directory paths for the live build
mkdir -p kali-config/common/includes.chroot/usr/share/wallpapers/kali/contents/images/
mkdir -p kali-config/common/includes.chroot/etc/apt/apt.conf.d/
mkdir -p kali-config/common/includes.chroot/etc/xdg/autostart/
mkdir -p kali-config/common/includes.chroot/usr/share/icons/cw/
#mkdir -p kali-config/common/includes.chroot/root/Desktop
#mkdir -p kali-config/common/includes.chroot/opt/

# Copy GpuTest to Live Build
#cp /opt/GpuTest kali-config/common/includes.chroot/opt/

# BUG Copy all the desktop Icons onto Live image
#cp ~/Desktop/* kali-config/common/includes.chroot/root/Desktop/

# copy file from user provided locations
cp $DESKTOP_WALLPAPER kali-config/common/includes.chroot/usr/share/wallpapers/kali/contents
cp $ICON_CACHE/* kali-config/common/includes.chroot/usr/share/icons/cw/


# grab the local Favorites bar before building the script below
FAVORITES=$(dconf read /org/gnome/shell/favorite-apps)
echo "Setting up favorites bar with $FAVORITES"
# We add a chroot hook and set up the wallpaper
# BUG: this isnt actualy setting any of the user customizaions durring the image process.
# still broken >..<
echo building files..........

cat > kali-config/common/hooks/gnome.chroot <<EOF
#!/bin/sh

set -e

# Set background and interface theme
dbus-launch --exit-with-session gsettings set org.gnome.desktop.background picture-uri 'file:///usr/share/wallpapers/kali/contents/images/Background.png'

# Set favorites bar to reflect the local system
dbus-launch --exit-with-session gsettings set org.gnome.shell favorite-apps "$FAVORITES"

EOF

# Set up custom packages here for building the ISO
cat <<EOF > kali-config/variant-gnome/package-lists/cw.list.chroot
# Tools used by Computer Wherehouse

# Forensics tools
gddrescue
ddrescueview

# Bare metal backup / Forensics Imaging
# package lookup seems to be broken on the preconfigured repositories for clonezilla
#clonzilla

# Drive testing
gsmartcontrol

# Resource usage
htop
gdmap
ncdu

# Stress Testing
stress

# Hardware information
hardinfo
lm-sensors

# Windows Networking compatibility
cifs-utils

# Anti-virus Software
clamav

# VNC Network Client and remote desktop
vinagre

# possible application/libraries
#libblkid-dev

# precision calculator
bc

#Python library installer for some package dependancies
python-pip

EOF

# Setup some aliases to add defualt options or short commands here

cat <<EOF > kali-config/common/includes.chroot/root/.bash_aliases
# Use dcfldd for more information instead of dd grab a size of our input file and provide a time estimate + percent done
alias dd='dcfldd sizeprobe=if'

# Show mount points in a nice Table
alias showfs='(printf "Device Mountpoint File_System_Type\n"; mount | cut -d " " -f 1-5 | sed "s:on::g" | sed "s:type::g") | column -t'

# Resume wget by default
alias wget='wget -c'

# Setup defualts for Rsync
# --prune-empty-dirs
# the /etc/rsync_exclude.conf should be built sepratly
# --no-OPTION will turn off the permissions, groups, and owner so we can do a straight copy to an NTFS based file system with not issues
alias rsync='rsync --partial --progress --times --recursive --compress --human-readable --verbose --no-perms --no-group --no-owner --exclude-from "/etc/rsync_exclude.conf"'

# Show Devices currently attached to system. Set some defualt values to display
alias lsblk='lsblk -o name,label,size,fstype,model'

# Set up some defualt options for Clam AV
# (Recursive scan, sound a bell on Positive detections)
# make a directory and move viruses to the clam_vault at the base of the scan
alias clamscan='mkdir ./clam_vault; clamscan --recursive=yes --bell --move=./clam_vault'

# Setup ddrescue defualts
# (Direct disk access, Force overwrite, Reopen the Drive on Error, and set the default copy size to 1024)
# 1024 cluster size with the --no-scrape --no-trim --cpass=1 options makes a fairly decent block by block cloner
alias ddrescue='clear; ddrescue --direct --force --verbose --reopen-on-error --cluster-size=1024'

# Setup diff color by defualt
alias diff='diff --color=always'

EOF

# Case insensitive Regular Expression matching for Windows names >..<
# Ignores hibernation file, Pagefile, temporary files, temp internet files, HitmanPro, Windows Prefetch, and cookies.
cat <<EOF >kali-config/common/includes.chroot/etc/rsync_exclude.conf
[Hh][Ii][Bb][Ee][Rr]Ff][Ii][Ll].[Ss][Yy][Ss]
[Pp][Aa][Gg][Ee][Ff][Ii][Ll][Ee].[Ss][Yy][Ss]
[Ww][Ii][Nn][Ss][Xx][Ss]/*
[Oo][Ll][Dd] [Ff][Ii][Rr][Ee][Ff][Oo][Xx] [Dd][Aa][Tt][Aa]
[Pp][Rr][Oo][Gg][Rr][Aa][Mm][Dd][Aa][Tt][Aa]/[Hh][Ii][Tt][Mm][Aa][Nn][Pp][Rr][Oo]
*.[Tt][Mm][Pp]
cookies
temporary internet files
windows/prefetch
hiberfil.sys
winsxs/*
EOF

cat <<EOF >kali-config/common/includes.chroot/root/.selected_editor
# Generated by /usr/bin/select-editor
SELECTED_EDITOR="/bin/nano"
EOF

cat <<EOF > kali-config/common/includes.chroot/etc/apt/apt.conf.d/80http
Acquire::http::No-Cache true;
Acquire::http::Pipeline-Depth 0;
EOF

cat <<EOF > kali-config/common/includes.chroot/etc/apt/apt.conf.d/99compression-workaround
Aquire::CompressionTypes::Order::"gz";
EOF

# Add mount points and automount data drives
# Update ClamAV on boot
cat <<EOF > kali-config/common/includes.chroot/etc/rc.local
#!/bin/bash

# Make the mount paths
mkdir -p /media/cw
mkdir -p /media/tech
mkdir -p /media/data

# Get ethernet online
ifup eth0

# Mount CW NAS shares providing username/password and mount points durring boot
mount.cifs //nas/data -o username=root,password=cw8400 /media/data
mount.cifs //nas/tech -o username=root,password=cw8400 /media/tech
mount.cifs //nas/cw   -o username=root,password=cw8400 /media/cw

# Grab a fresh clam av database in the background ( updates )
# This update could take a while
freshclam -v&
EOF

chmod a+x kali-config/common/includes.chroot/etc/rc.local

# XDG Autostart desktop applications
cat <<EOF > kali-config/common/includes.chroot/etc/xdg/autostart/Gsmart.desktop
[Desktop Entry]
Name=GSmart
GenericName=Hdd Diagnostics
Comment=Auto start the Gsmart Control HDD Diagnostics system on start
Exec=/usr/bin/gsmartcontrol
Terminal=false
Type=Application
X-GNOME-Autostart-enabled=true

EOF

# Sludgehammer tactic Pull the entire .config directory from current system and drop it into the Live Image
# BUG: chroot hooks dont seem to be excecuted properly so were cloning the entire working environment
echo rebuilding profiles

cp -rf ~/.config kali-config/common/includes.chroot/root/

echo changing permissions

chmod 755 kali-config/common/hooks/gnome.chroot

# Run the build
./build.sh --distribution kali-rolling --verbose
