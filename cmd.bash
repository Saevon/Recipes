
# Reading Japanese Files
iconv -f SHIFT_JIS -t utf-8 "Read me.txt" > UTF8-Readme.txt 
# Also, try opening file in chrome, and view >> encodings...


# Python env Fix
export ARCHFLAGS="-Wno-error=unused-command-line-argument-hard-error-in-future"

# Get space of folders
du -hs .[!.]* *

# Hide File (Mac)
sudo chflags hidden $FILE

# Fix Duplicate “Open With”
/System/Library/Frameworks/CoreServices.framework/Versions/A/Frameworks/\LaunchServices.framework/Versions/A/Support/lsregister -kill -r -domain local -domain user

# Mac Incrementl Adjust: Opt-Shift (vol, bright)
