from subprocess import STDOUT,  PIPE, Popen, check_output, CalledProcessError

# TODO 3 rename test.py to pathbuilder.py
# make sure these work

# module functions as follows:
# Get entire tree starting from path and return
# Mkdir of path starting from newpath

# can we please stop using Popen and subprocess for EVERYTHING i mean i know its great but holy crap overboard much?
def GetTree(path='/mnt'):
    """Gets a file tree"""
    disk.prog.find[1]=path
    find = Popen(disk.prog.find, stdout=PIPE, stderr=PIPE)
    out, err = find.communicate()
    return([s.strip() for s in out.splitlines()])

# TODO 4 more pythonic way of doing this?
def SetTree(newpath):
    """Rebuilds file tree at path"""
    disk.prog.mkdir[2] = newpath
    mkdir = Popen(disk.prog.mkdir, stdout=PIPE, stderr=PIPE)
    out, err = mkdir.communicate()

def list_files(startpath):
    """Grab directory tree from startpath"""
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))