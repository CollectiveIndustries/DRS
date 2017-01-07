#!/usr/bin/env python

import json
import subprocess

block_list = ['lsblk', '--json', '-nd', '-o', 'name,size,model,serial']

dsk = subprocess.Popen(block_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

out, err = dsk.communicate()

try:
    decoded = json.loads(out)

    # Access data
    for x in decoded['blockdevices']:
        print "Drive: "+x['name']+" is "+x['size']

except (ValueError, KeyError, TypeError):
    print "lsblk returned the wrong JSON format"
