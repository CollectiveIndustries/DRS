class prog:
	umount = ['umount']
	lsblk = ['lsblk', '--json', '--noheadings', '-o', 'name,size,model,serial,fstype,label']
	rsync = ['rsync', '--recursive', '--compress-level=9', '--human-readable', '--progress', '--no-perms', '--no-owner', '--no-group', '--no-times', '--ignore-existing', '--exclude-from=/etc/rsync_exclude.conf']
	cp = ['cp', '/media/cw/Drew/Live_USB/scripts/rsync_exclude.conf', '/etc/rsync_exclude.conf']
	ntfs = ['lowntfs-3g', '-o', 'windows_names,ignore_case']
	cifs = ['mount', '-t', 'cifs', '-o', 'username=root,password=cw8400', '//192.168.0.241/data', '/media/data']
	NtfsFix = ['ntfsfix', '--clear-bad-sectors', '--clean-dirty']

# class container for Ignore lists
# TODO set up regex for these to avoid adding loop0 loop1...loopX

class ignore:
	filesystems = ['iso9660', 'squashfs', 'crypto_LUKS', None, 'swap']
	devices = ['sr0', 'sr1', 'loop0', 'mmcblk0boot0', 'mmcblk0boot1', 'mmcblk0rpmb']

# This class provides the functionality we want. You only need to look at
# this if you want to know how this works. It only needs to be defined
# once, no need to muck around with its internals.
# Located at http://code.activestate.com/recipes/410692/
class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args:
            self.fall = True
            return True
        else:
            return False


# Text output color definitions
class color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
