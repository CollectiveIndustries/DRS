#!/bin/bash

# Set Common Config variables here
LAN_ADDY=192.168.0.0/24
DESKTOP_WALLPAPER=/media/cw/Drew/Live_USB/background/Background.png
USB_SPLASH=/media/cw/Drew/Live_USB/background/cwsplash.png
ICON_CACHE=/usr/share/icons/cw
VARIANT=light
ARCH=i386
GCONF_OVERRIDES=/usr/share/glib-2.0/schemas/

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
mkdir -p kali-config/common/includes.chroot/home/user/Desktop
mkdir -p kali-config/common/includes.chroot/usr/share/icons/cw/
mkdir -p kali-config/common/includes.chroot/opt/cw/shared

#mkdir -p kali-config/common/includes.chroot/opt/

# Copy files from local repository into live FileSystem
cp ../DRS/Fddrescue/sync.py kali-config/common/includes.chroot/opt/cw/backup
cp ../DRS/Fddrescue/rescue.py kali-config/common/includes.chroot/opt/cw/rescue
cp ../DRS/Fddrescue/shared/*.py kali-config/common/includes.chroot/opt/cw/shared/

# Grab network hosted configuration settings
cp /media/cw/Drew/Live_USB/scripts/rsync_exclude.conf kali-config/common/includes.chroot/etc/rsync_exclude.conf

# BUG Copy all the desktop Icons onto Live image
#cp ~/Desktop/* kali-config/common/includes.chroot/root/Desktop/

# copy file from user provided locations
cp $DESKTOP_WALLPAPER kali-config/common/includes.chroot/usr/share/wallpapers/kali/contents/Background.png
cp $ICON_CACHE/* kali-config/common/includes.chroot/usr/share/icons/cw/


# grab the local Favorites bar before building the script below
FAVORITES=$(dconf read /org/gnome/shell/favorite-apps)
echo "Setting up favorites bar with $FAVORITES"
# We add a chroot hook and set up the wallpaper
# BUG: This isnt actualy setting any of the user customizaions durring the image process.
# still broken >..<
echo building files..........

cat > kali-config/common/hooks/gnome.chroot <<EOF
#!/bin/sh

set -e

# Set background and interface theme
dbus-launch --exit-with-session gsettings set org.gnome.desktop.background picture-uri 'file:///usr/share/wallpapers/kali/contents/Background.png'

# Set favorites bar to reflect the local system
dbus-launch --exit-with-session gsettings set org.gnome.shell favorite-apps "$FAVORITES"

EOF

# Set up custom packages here for building the ISO
cat <<EOF > kali-config/variant-$VARIANT/package-lists/cw.list.chroot
# Tools used by Computer Wherehouse

# Partition tools
gparted
ntfs-3g

# Password reset for windows
chntpw

# Forensics tools
gddrescue
ddrescueview

# Bare Metal Backups
# package lookup seems to be broken on the preconfigured repositories for clonezilla
#clonzilla

# Drive testing
gsmartcontrol

# Resource usage
htop
ncdu

# Windows Networking compatibility
cifs-utils

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
alias rsync='rsync --partial --progress --times --recursive --compress --human-readable --verbose --no-perms --no-group --no-owner --no-times --exclude-from "/etc/rsync_exclude.conf"'

# Show Devices currently attached to system. Set some defualt values to display
alias lsblk='lsblk -o name,label,size,fstype,model'

# Setup ddrescue defualts
# (Direct disk access, Force overwrite, Reopen the Drive on Error, and set the default copy size to 1024)
# 1024 cluster size with the --no-scrape --no-trim --cpass=1 options makes a fairly decent block by block cloner
alias rescue='clear; ddrescue --idirect --odirect --force --verbose --reopen-on-error --cluster-size=1024'

# Setup diff color by defualt
alias diff='diff --color=always'

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
cat <<EOF > kali-config/common/includes.chroot/etc/rc.local
#!/bin/bash

# Make the mount paths
mkdir -p /media/cw
mkdir -p /media/tech
mkdir -p /media/data

# Mount CW NAS shares providing username/password and mount points durring boot
mount -t cifs //192.168.0.241/data -o username=root,password=cw8400 /media/data
mount -t cifs //192.168.0.241/tech -o username=root,password=cw8400 /media/tech
mount -t cifs //192.168.0.241/cw   -o username=root,password=cw8400 /media/cw
EOF


# XDG Autostart desktop applications
cat <<EOF > kali-config/common/includes.chroot/home/user/Desktop/Gsmart.desktop
[Desktop Entry]
Name=GSmart
GenericName=Hdd Diagnostics
Comment=Auto start the Gsmart Control HDD Diagnostics system on start
Exec=/usr/bin/gsmartcontrol
Terminal=false
Type=Application
X-GNOME-Autostart-enabled=false

EOF

# Sludgehammer tactic Pull the entire .config directory from current system and drop it into the Live Image
# BUG: chroot hooks dont seem to be excecuted properly so were cloning the entire working environment
echo rebuilding profiles

#cp -rfv ~/.config kali-config/common/includes.chroot/home/user/

echo changing permissions

chmod 755 kali-config/common/hooks/live/gnome.chroot
chmod a+x kali-config/common/includes.chroot/etc/rc.local
chmod a+x kali-config/common/includes.chroot/opt/cw/rescue
chmod a+x kali-config/common/includes.chroot/opt/cw/backup

echo running verbose build
# Run the build
./build.sh --distribution kali-rolling --verbose --variant $VARIANT --arch $ARCH

# Copy the ISO image to the ISO directory mount the ISO as a loop and copy the files out to the PXE_Server web root folder
umount /mnt/loop
mount images/kali-linux-$VARIANT-rolling-$ARCH.iso /mnt/loop

cp -v /mnt/loop/live/filesystem.squashfs /var/www/html/live/kali/filesystem.squashfs

umount /mnt/loop

echo Build finished
