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
/System/Library/Frameworks/CoreServices.framework/Versions/A/Frameworks/LaunchServices.framework/Versions/A/Support/lsregister -kill -r -domain local -domain user

# Python env Fix
export ARCHFLAGS="-Wno-error=unused-command-line-argument-hard-error-in-future"

# remove all those ._* files
dot_clean .

# Get battery status
pmset -g batt | { read; read n status; echo "$status"; }

# Mac Incremental Adjust:
    Opt-Shift (vol, bright)


# Saying things to other Audio Devices
say -r160 -a "AirPlay" "hello world"
# get a list of all valid audio devices
say -a?

# Dictionary location
/Users/<user>/Library/Spelling/LocalDictionary
/usr/share/dict/words


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


# Disk Management

# Partition a Drive
diskutil partitionDisk ${Disk:/dev/disk3} ${NumDisks:2} GPT ... (see below)
    HFS+ Boot 25%
    ExFat Images R







###########################################
# Misc
##########################################

# Help for directories
man hier

# Get full help for anything (any aliases, functions, and location of binaries)
type -a name

# SUDO keep paths
sudo env "PATH=${PATH}" cmd


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
# Show permissions of the entire path
namei -ml <path>


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

# File Handles / Inodes
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
setfacl -m u:username:rw ./file.ext
getfacl <directory>

# Pretty print json from a site (or file)
python -m json.tool <(curl rest.site.com/uri/)
python -m json.tool < $FILE


# Add colours to logs (replace the echo with the log command
BLUE=`echo -e "\e[36m"` && END=`echo -e "\e[39m"`
echo "2016-01-01-app hello" | sed -E "s/([0-9]{4}-[0-9]{2}-[0-9]{2}[^ ]*)/$BLUE\1$END/g"


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

# Resize with white border
# (SVG example)
convert $IN.svg -resize 28x    -gravity center -extent 32x32   $OUT.png

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







