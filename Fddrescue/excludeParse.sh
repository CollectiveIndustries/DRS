#!/bin/bash

# runs the exclude list through sed to drop all letters to lowercase.
sed -i 's/.*/\L\1/g' rsync_exclude.conf
