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





###########################################
# Misc
##########################################

# Get space of folders
du -hs .[!.]* *

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


# See all open ports on machine
# without sudo this only shows your processes
sudo lsof -PiTCP -sTCP:LISTEN




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
