import pathlib
import os
import math

# Mount drive (/mnt)

# Get customer name from tech

def ReadableSize(fstat):
    """Convert file size to MB, KB or Bytes"""
    if (fstat.st_size > 1024 * 1024):
        fsize = math.ceil(fstat.st_size / (1024 * 1024))
        unit = "MB"
    elif (fstat.st_size > 1024):
        fsize = math.ceil(fstat.st_size / 1024)
        unit = "KB"
    else:
        fsize = fstat.st_size
        unit = "B"
    return fsize, unit

def RecoverDirTree(oldPath, newPath):
    """Grab directory tree from startpath"""
    for (root,dirs,files) in os.walk(oldPath):
        MkPath = '{}'.format(root.replace(oldPath,newPath,1))
        pathlib.Path(MkPath).mkdir(parents=True, exist_ok=True) # Create Target DIR

        for f in files: # for each file in old path ddrescue to newpath
            OldFile = '{}/{}'.format(root,f)
            NewFile = '{}/{}'.format(root.replace(oldPath,newPath,1),f)
            fsize, unit = ReadableSize(os.stat(os.path.join(root,f)))
            
            # Print file attributes
            print('{:20s}{:8d} {:2s}'.format(f,fsize,unit))

            # TODO call DDRescue
            print("ddrescue OPTIONS {} {} MAPFILE".format(OldFile,NewFile))

# tee tmp log to screen + rescue log
