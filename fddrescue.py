
cat listoffiles | while read file
pipe while> do
pipe while> ls -l "$file"
pipe while> ddrescue -n -e1  "$file" /cc/RecoveredFiles/"$file" /cc/RecoveredFiles/"$file".llog
pipe while> date
done | tee -a  /cc/RecoveredFiles/ddrescue.log

# Identify mountable drive. (fdisk -l)

# Mount drive (/mnt)

# Scan folder tree

# Get customer name from tech

# mkdir for recovery [NAME Date (mm-dd) Tech]

# mkdir path for directory tree

# get list of files from source tree W/ path

# run ddrescue $FILE destination/$FILE tmp.llog

# tee tmp log to screen + rescue log
