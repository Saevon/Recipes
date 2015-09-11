##########################
# Mac
##########################

# Hide File
sudo chflags hidden $FILE

# Fix Duplicate “Open With”
/System/Library/Frameworks/CoreServices.framework/Versions/A/Frameworks/\LaunchServices.framework/Versions/A/Support/lsregister -kill -r -domain local -domain user

# Python env Fix
export ARCHFLAGS="-Wno-error=unused-command-line-argument-hard-error-in-future"

# Mac Incrementl Adjust: Opt-Shift (vol, bright)



# Set default permissions under a directory
# MAC ONLY: Unix uses setfacl (see unix section below)

# Read ACL
ls -le
# Write ACL
chmod +a 'group allow <permissions>' <directory>
chmod +a 'group deny <permissions>' <directory>
chown Saevon:self <directory>
chmod u=rwX,g=rwX,o= <directory>
# Clear ACL
chmod -N <directory>

# Working with Extended Attributes (the @)
ls -l@
# clear all
xattr -c
# delete one
xattr -d <attribute>



# Fast user Switching
# to Login Window
/System/Library/CoreServices/Menu\ Extras/User.menu/Contents/Resources/CGSession -suspend
#Specific User
/System/Library/CoreServices/Menu\ Extras/User.menu/Contents/Resources/CGSession -switchToUserID `id -u $USERNAME`


# Restart Audio Service, get the pid
ps aux | grep coreaudio

# Fast user Switching
# to Login Window
/System/Library/CoreServices/Menu\ Extras/User.menu/Contents/Resources/CGSession -suspend
#Specific User
/System/Library/CoreServices/Menu\ Extras/User.menu/Contents/Resources/CGSession -switchToUserID `id -u $USERNAME`


# Restart Audio Service, get the pid
ps aux | grep coreaudio


###########################################
# Misc
##########################################

# Get space of folders
du -hs .[!.]* *

# Show the directory permissions, not contents
ls -d ~
ls -ld ~

# Terminal notification (number)
tput bel

# Add commands to running process
#<Ctrl-Z>: aka pause the job
fg && tput bel

# Reading Japanese Files
iconv -f SHIFT_JIS -t utf-8 "Read me.txt" > UTF8-Readme.txt
# Also, try opening file in chrome, and view >> encodings...


# Makes a job a daemon (won't quit on terminal exit)
disown -h


# XARGS: command2 will get the entire output as args (replacing \n with space)
command | xargs command2
# XARGS: for files with spaces (replace show_args.py with your
find . -name "*.mp3" -print0 | xargs -I{} -0 ~/Projects/Recipe/show_args.py {}
# XARGS: you can have it display the command run with -t
echo a b c | xargs -t -n 1 echo


# See all open ports on machine
# without sudo this only shows your processes
sudo lsof -PiTCP -sTCP:LISTEN


# Set default permissions under a directory
# UNIX ONLY: Mac uses chmod (see mac section above)
setfacl <directory>
getfacl <directory>


# CronTab times
# *     ~ all values
# 1,4   ~ 1 and 4
# 3,9/2 ~ from 3 to 9 with a step of 2 (aka 3,5,7,9)
# */3   ~ all values with a step of 3
# 
# Special values are also allowed
# @reboot
# @yearly/@annually
# @monthly
# @weekly
# @daily/@midnight
# @hourly

# generate private key from public key
ssh-keygen -y -f id_rsa -C "serghei@Windy" > id_rsa.pub


#################################################
# Bash Syntax
#################################################

# If statements
if [ $? -ne 0 ]; then
    ...
fi
# equivalent to:
if command; then : ; else
    ...
fi


# Bash file reading, if you use backticks, you might reach the ARG_MAX
#   which is the maximum number of characters a command can be in term
while read f; do
    ...
done <file
# OR
command |
while read f; do
    ...
done

# SIGNALS:
# SIGINT: Ctrl-C
# SIGTERM: exit
# SIGQUIT: exit + coredump
# SIGHUP: terminal death (hangup), use nohup to cause a thing not to exit on this
# SIGINT: Immediate kill
# Proper kill (give each some time): TERM, INT, UP, KILL
