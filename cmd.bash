# (Don't run this stuff...)
exit 0

##########################
# Mac
##########################

# toggle root user
dsenableroot -u $USER
dsenableroot -d -u $USER

# Reset passwd in single user mode
fsck -fy
mount -uw /
launchctl load /System/Library/LaunchDaemons/com.apple.opendirectoryd.plist
passwd $username

# Hide File
sudo chflags hidden $FILE
sudo chflags nohidden $FILE
# This also creates a `._$FILE` for the metadata, useful for non HFS+
SetFile -a V $FILE
SetFile -a v $FILE

# Hide files in windows
attrib +H +S FILE

# clipboard
pbcopy
pbpaste
# custom alias that removes attributes from clipboard
pbclean


# Fix Duplicate “Open With”
/System/Library/Frameworks/CoreServices.framework/Versions/A/Frameworks/\LaunchServices.framework/Versions/A/Support/lsregister -kill -r -domain local -domain user

# Python env Fix
export ARCHFLAGS="-Wno-error=unused-command-line-argument-hard-error-in-future"

# remove all those ._* files
dot_clean .

# Mac Incremental Adjust: Opt-Shift (vol, bright)


# Saying things to other Audio Devices
say -r160 -a "AirPlay" "hello world"
# get a list of all valid audio devices
say -a?


# Set default permissions under a directory
# MAC ONLY: Unix uses setfacl (see unix section below)

# Dictionary location
/Users/<user>/Library/Spelling/LocalDictionary
/usr/share/dict/words

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
# unquarantine a folder/app
xattr -rd com.apple.quarantine .
# Read the source of a downloaded file
#   this needs the kMDItemWhereFroms attr to be set
xattr -p com.apple.metadata:kMDItemWhereFroms "$file" | xxd -r -p | plutil -convert xml1 -o - -
mdls -name kMDItemWhereFroms $file



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

# Menubar: audio
⌥(opt) click:   change audio devices
⇧(shift) click: change alert volume
⌥(opt) + fn key: opens the system preferences menu for that fn (e.g. brightness, sound)


# Open another copy of an app
open -n /Applications/$APP.app

# Open an app in /Applications
open -a $APP

# Force Quit an App
killall -HUP $NAME
⌥ ⌘ + esc

# Open in finder
# do this in the dock, or spotlight
⌘ + click/enter: opens the file/application in finder


# Edit the terminal title bar
echo -ne  "\033]0;$TITLE\007"
printf "\e]0;$TITLE\a"


###########################################
# Misc
##########################################

# SUDO keep paths
sudo env "PATH=${PATH}" cmd

# Sed
# POSIX space Char
sed s/^[[:space:]]*//

# Split a : seperated list then run a command on each item
lnks=
lnks+=:data
lnks+=:other
echo ${lnks} | sed s/^[[:space:]]*:// | tr : '\0' | xargs -0 -I {} echo link {}

# Clean out duplicates in history
history | nl | sort -k 2 -k 1,1nr | uniq -f 1 | cut -f2 | history -w


# Map a command on files
# in this case it echoes the file, then the file without the pdf extension
find . -name "*.pdf" -exec sh -c 'echo $0, ${0%.pdf}' {} \

# Get space of folders
du -hs .[!.]* *

# Create large Files:
# Sparse File (or normal ones in mac)
dd bs=1 count=0 seek=4g of=large_file.txt
# Linux
fallocate -l 4GiB large_file.txt

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


# Get the IP addresses of the machine
alias ipPublic="ip route get 8.8.8.8 || curl --silent http://icanhazip.com"
alias ips="ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}'"
# Gets IPS and the relevant interface
alias ips="ifconfig | perl -0 -pe 's/\n\t+/ /g' | awk -v RS="\n" '{match($0,"^[^:]+",interface); match($0, "([0-9]{1,3}\\.){3}[0-9]{1,3}",ip); if (ip[0] != "" && ip[0] != "127.0.0.1") { printf interface[0]; print ": "; print ip[0]}}'"

# See all open files
# lsof shows a shapshot, opensnoop monitors
sudo opensnoop
sudo opensnoop -p $PID
sudo opensnoop -f $FILE
lsof $FILE
lsof +D $DIR
lsof -u $USER
lsof -u ^$excluded_USER
lsof -p $PID

# kill all processes using a file
# -t outputs only the PID
kill -9 `lsof -t $FILE`


# Set default permissions under a directory
# UNIX ONLY: Mac uses chmod (see mac section above)
setfacl <directory>
getfacl <directory>

# Pretty print json from a site (or file)
python -m json.tool <(curl rest.site.com/uri/)
python -m json.tool < $FILE


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


# Add colours to logs (replace the echo with the log command
BLUE=`echo -e "\e[36m"` && END=`echo -e "\e[39m"`
echo "2016-01-01-app hello" | sed -E "s/([0-9]{4}-[0-9]{2}-[0-9]{2}[^ ]*)/$BLUE\1$END/g"



##############################################
# Mail
#############################################
# postfix
#  https://blog.anupamsg.me/2012/02/14/enabling-postfix-for-outbound-relay-via-gmail-on-os-x-lion-11/


# restart
postfix reload
launchctl stop org.postfix.master
launchctl start org.postfix.master

# logs
tail -f /var/log/mail*

# check the config
postconf -n

cd /etc/postfix
vim ./main.cf
vim ./aliases
vim ./generic
sudo chmod 600 sasl.passwd
vim sasl.passwd
vim /System/Library/LaunchDaemons/org.postfix.master.plist
launchctl unload -w /System/Library/LaunchDaemons/org.postfix.master.plist
launchctl load -w /System/Library/LaunchDaemons/org.postfix.master.plist


# reload the configs
postfix reload
postmap generic
postmap sasl.passwd

# delete mail
postsuper -d ALL
# delete deferred mail
postsuper -d deferred

# view queue
postqueue -p
# Retry all mail
postqueue -f



#################################################
# Bash Syntax
#################################################



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

###################
# SIGNALS:
# SIGINT: Ctrl-C
# SIGTERM: exit
# SIGQUIT: exit + coredump
# SIGHUP: terminal death (hangup), use nohup to cause a thing not to exit on this
# SIGINT: Immediate kill
# Proper kill (give each some time): TERM, INT, UP, KILL


############################
# Variables
echo "# path to me --------------->  ${0}     "
echo "# parent path -------------->  ${0%/*}  "
echo "# my name ------------------>  ${0##*/} "

$@ all positional arguments
$* all positional arguments
$# number of positional args
"$@" all arguments as individually quoted
    cmd 'a' 'b c d' e => "$@" => "a" "b c d" "e"
"$*" all arguments quoted as a chunk
    cmd 'a' 'b c d' e => "$*" => "a b c d e"

$0 me
$1-$N my args
${@:3} my args 3-N

$$      your PID
${PPID} PPID
$!      PID of the last background command (run with &)


################
# variable substitution

# ":" makes the command also replace values that are declared, but empty
# this works in all the subsequent commands
${var:-default}

# Default value
${var-default}  substitute with string "default" if var is undeclared
${var-$default} substitute with $default if var is undeclared

# default value, and set variable
${var=default}  sets the variable to the given string if undeclared

# replace value if set
${var+default} Outputs the default only if var is not undeclared
${var:+default} Outputs the default if var is neither undeclared nor empty

# Error out if set
${var?err_message}


# Variable length
${#var}

# Regexp
${var#regexp}   remove shortest match from front
${var##regexp}  remove longest match (greedy) from front
${var%regexp}   remove shortest match from back
${var%%regexp}  remove longest match (greedy) from back
${var/regexp/replace}   replace
${var/#regexp/replace}  replace matching front
${var/%regexp/replace}  replace matching back
${var//regexp/replace}  global replace


# Substr
${var:3}   from [3:]
${var:3:2} from [3:5] (second param is length)


# programmatic var names
${!prefix*} get all variable names starting with prefix
${!prefix@}
${!var}     expand the variable $var, then expand that as a variable name
    b=12 a=b ${!a} => 12






##############
# If statements

if [ $? -ne 0 ]; then
    ...
fi
# equivalent to:
if command; then : ; else
    ...
fi

# Extended Test: Operators
[[ ]]

# return the exit status
# used to do C style math
$(( ))

# VAR++, VAR--: post increment
# ++VAR, --VAR: pre increment
# + -, * / %
# ** exponents
# ==, !=, <, >, <=, >=
# ! && ||
# ~ & | ^: bitwise


&& # -a in [ ]
|| # -o in [ ]
# Integer OCmparison
-eq -ne -gt -ge -lt -le
# String Comparison
== != < > >= <=
=~ "$REGEXP"
-n # Not Null: Note wierd reactions with $@
-z # Null

# negation
# Note that e.g. [ ! -d ] would pass non directories, and non-existing files
[ ! ... ]

# Passes symlinks
[ -a "$EXISTS" ]
[ -d "$DIR" ]
[ -L "$SYMLINK" ]
[ -f "$FILE" ]
[ -e "$ARCHIVE" ]
[ -h "$SYMLINK" ]
[ -O "$FILE" ] # owned by current User
[ -G "$FILE" ] # owned by current Group
[ -r | -x | -w ] # Permissions tests


# OS Detection
if [[ "$OSTYPE" == "linux-gnu" ]]; then
        # ...
elif [[ "$OSTYPE" == "darwin"* ]]; then
        # Mac OSX
elif [[ "$OSTYPE" == "cygwin" ]]; then
        # POSIX compatibility layer and Linux environment emulation for Windows
elif [[ "$OSTYPE" == "msys" ]]; then
        # Lightweight shell and GNU utilities compiled for Windows (part of MinGW)
elif [[ "$OSTYPE" == "win32" ]]; then
        # I'm not sure this can happen.
elif [[ "$OSTYPE" == "freebsd"* ]]; then
        # ...
else
        # Unknown.
fi



# Local Variables
local var=1


# Arrays
array=()
array[0]=a
# get length
${#array[@]}
# print entire array
${array[@]}
# slice: takes 2 elements starting from element 3
${array[@]:3:2}
# slice: after taking an element, slices the elemnt in index one
${array[1]:3:2}



#################
# Images & PDF
#################
# General Command: comes from the imagemagick library
convert
# OSX specific:
sips -s format png $IN.jpg --out $OUT.png


# Change Brightness/Contrast
# Increase Contrast (note the + means decrease ...), it is repeatable for a more pronounced effect
convert $IN.jpg $OUT.jpg -contrast
convert $IN.jpg $OUT.jpg +contrast
# Change Contrast/Brightness: values are from -100,100 with 0 being no change
convert $IN.jpg $OUT.jpg -brightness-contrast $bright,$contrast

# Resize
convert $IN.jpg $OUT.jpg -resize

# Change Bookmarks/TOC in pdf
# Note: binary name changed by me from jpdfbookmarks
pdfbookmarks --apply bookmarks.txt --out $OUT.pdf $IN.pdf
pdfbookmarks --dump $IN.pdf --out bookmarks.txt




#########################################
# Audio & Music & Video
########################################

# Fix bad encodings: $encoding: the encoding you think the files are
find . -iname "*.mp3" -execdir mid3iconv -e $encoding {} \;

# Add a second of silence to the beginning of the file
# the 1 0 is seconds of silence at the begginning then the end
find . -name "*!(.pad).wav" -exec sh -c 'sox "$0" "${0%.wav}.pad.wav" pad 1 0' {} \

# To guess at encodings, choose a file and try this:
mid3iconv -dp -e $encoding $file
# Try the following:
# Cyrillic: 1251-ANSI
# Japanese: JIS

# Video: webm
 ffmpeg -i "input.webm" -c:v libx264 -c:a aac -strict experimental -b:a 192k output.mp4
# convert webm with mp4s (keeping both)
 find . -name "*.webm" -exec sh -c 'ffmpeg -i "$0" "${0%.webm}.mp4" -c:v libx264 -c:a aac -strict experimental -b:a 192k' {} \;





########################################
# Vim
########################################

# If this returns -clipboard, you can't copy to clipboard
# (registers @ or + )
vim --version | grep '+clipboard'

# exit vim with an error code (e.g. during git commit to abort)
:cq



########################################
# Terminal commands
########################################

Ctrl-c: SIGINT
Ctrl-d: EOF
Ctrl-z: SIGSTOP (see %1, jobs, fg, bg, &)

Ctrl-a: beginning of line
Ctrl-e: end of line

# warning: needs to be enabled in temrinal "option as meta key"
Alt-b: forward a word
Alt-f: back a word

Ctrl-p: back in history
Ctrl-n: forward in history

# In bash Vi mode, press "v" in command mode
Ctrl-x e: edit line in $EDITOR

# Type twice to cycle through completions
Ctrl-r: reverse search
Ctrl-l: clear screen



############
# History
!!:  previous command
!12: 12 command in history
!-2: second to last command in history
!*:  get all args
!-2*

# first command that starts with string
!string
# first command containing string
!?string?
# regexp in command
!!:gs/txt/mp3/

# fix previous command
echo mistaken/file/path
^mistaken^better

# Clear bash command cache (hashtable)
hash -r

# Force bash to check hashed entries
shopt -s checkhash


###########################
# Process/file substitution

# puts the result of the echo command into a tmp-file (named pipe) and passes it to command as a filename ~(/dev/fd/64)
command <(echo yay)
# creates a named pipe for command to write to (e.g. a command that accepts a logfile). Then instead of writing to a file, the grep command gets the data
# aka converts file only output to stdout
command >(grep "error")

# Pipes stdout and stderr to seperate commands
command > >(tee info.log) 2> >(tee err.log >&2)
# Expands to this:
command > /dev/fd/63 2> /dev/fd/64
# Remember: tee outputs to both a file and stdout.
# Thus outputs to both stdout, stderr and the two individual files

# Partial Permissions
command >(sudo tee info.log >/dev/null)
command >(sudo dd of=info.log)


#################
# Brace Expansion

echo --{a..d}
--a --b --c --d
echo --{1..5}
--1 --2 --3 --4 --5
echo --{,2,a}
-- --2 --a

# Bash 4: adds steps
echo --{1..10..3}
--1 --4 --7 --10

# Nesting
echo {{A..Z},{a..z}}
echo {,{0..2},{a..c}}
-- --0 --1 --2 --a --b --c

# Matrix: all possible expansions
echo {test,prod}/{,usr/,usr/local/}{{,s}bin,etc,lib,share}

# Math outputs the '-v' 3*3*3 times (27)
echo -v{,,}{,,}{,,}

# Number padding
echo 00{1..9} 0{10..99} {100..999}
# Bash 4
echo {001..999}


##################
# Completions
complete -A $TYPE [$CMDS...]
-A command
-A function
-A variable
-A alias
-A builtin
-A signal

-A setopt
-A shopt
-A binding

-A job
-A running
-A stopped
-A service

-A helptopic

-A user

-A directory
-A file


##############
# Directory Expansion & Globs

# Home directory
~
# CWD
~+
# Parent of CWD
~-


#######################
# Redirections

# Command Substitution (puts output in place)
echo `cmd`
echo $(cmd)

# Redirect (pipe) to stdout
cmd | cmd2
# Send on stderr through pipe
echo 2>&1 | cmd2
# Bash 4.0, Deprecated
echo |& cmd2

# Redirect to File
echo > filename
# Redirect both to file
echo 2>&1 > filename
# Redirect both to file, Deprecated
echo &> filename
# Dump stdout
echo > /dev/null
# Append to file
echo >> filename

# Redirect from file
echo < filename

# WARNING! opening a file with > truncates the file immediately

# Redirect from user input (Reads until the given symbol is typed 'EOL')
grep words << EOL
# Redirect from string, can be multiline
grep words <<< 'words go here'


# Order Matters!
# stderr -> original_stdout, stdout -> file
echo 2>&1 > filename
# stdout -> file, stderr -> new_stdout -> file
echo > file 2>&1

# Process Substitution
# creates a pipe, and outputs its location (filepath) as a string
# Thus allowing the program to pretend to read/write to a file

diff <(cmd1) <(cmd1)

# Duplicate output
tee >file | echo 'goes to both file and this command'
tee >(cmd1) >file | echo 'cmd1 and original stdout both get here (duplicated output)'
tee >(cmd1) >(cmd2) >/dev/null | echo 'both cmds stdout/stderr goes here'


# Permanent Redirections
exec > filename
exec > >(cmd)

# Creates a tmp fd 6, and backs up stdout
# Then makes stdout write to a file
exec 6>&1 > tmp.log
# This command now writes to the file
lsof -a -p $$ -d{0..99}
# Now we restore stdout cleaning up fd6
exec 1>&6 6>&-
# OR a shortversion
exec 1>&6-

# Named fd, note: if you delete said file, the fd breaks
exec {data}>data.log
cmd >&${data}

# Warning: >&- <&- close fd, and some programs will be very unhappy about that
# If you just want to ignore data from it redirect to /dev/null instead

# Swap stdout stderr
exec 3>&1 1>&2 2>&3 3>&-
exec 3>&1- 1>&2 2>&3-

# See current pipes
lsof -a -p $$ -d{0..99}
kill -9

# Messing around and seeing the results
# put any redirects in, and see how the first 99 fd are affected
# Only the ones that remain open are shown
# NOTE: 99 is used to ensure you can close fd1 (stdout) and still see what happens
# Warning: since lsof is in {} temporary fd will be opened as well (ignore those)
bash -c 'exec 99>&1; { lsof -a -p $$ -d{0..99} >&99; } $REDIRECTS'


# Special FD

# Black hole fd
/dev/null
# FD that writes null bytes
/dev/zero
# FD to current shell
/dev/tty





##############################
# Subshells
##############################

# Opens a subshell (both will have a different inner pid and pipes
x=false; ( x=true; ); echo $x === false
x=false; { x=true; }; echo $x === true
