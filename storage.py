# sorage module for mounting umounting drives
# remote file systems such as SMB/NFS/NAS

def NasMount(): # Needs refactoring Might be moved to a NAS Storage handler
    try:
        print("Mounting Storage Server....")
        err = check_output(RescueMount)
        print(com.color.OKGREEN+"Server Drive Mounted."+com.color.END)
        time.sleep(10)
    except CalledProcessError as ERROR:
        print(com.color.FAIL+"ERROR while mounting "+RescueMount[3]+'\nReturned with Error:\n>>>> '+str(ERROR)+com.color.END)
        exit(ERROR.returncode)
