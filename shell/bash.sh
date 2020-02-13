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


# -----------------------
# SIGNALS:
# SIGINT: Ctrl-C
# SIGTERM: exit
# SIGQUIT: exit + coredump
# SIGHUP: terminal death (hangup), use nohup to cause a thing not to exit on this
# SIGINT: Immediate kill
# Proper kill (give each some time): TERM, INT, UP, KILL

# -----------------------
# Orphans & the Init Process
#

# TODO:


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


# Indirect Variable
# Programmatic var names
${!prefix*} get all variable names starting with prefix
${!prefix@}
${!var}     expand the variable $var, then expand that as a variable name
    user_root="23ef0bc0dea0b-root-password"
    user_self="2099c090a9s09-my-password"
    user_bot="12309cb908ae09-bot-password"

    # You can now choose a variable by changing this
    login_user=user_

    # This now outputs: "2099c090a9s09-my-password"
    ${!login_user}






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




# Local Variables
local var=1


# --------------------------------
# Arrays
array=()
# Assign
array[0]='data'
# Append
array+=('new_data')
# get length
${#array[@]}
# print entire array
${array[@]}
# slice: takes 2 elements starting from element 3
${array[@]:3:2}
# slice: after taking an element, slices the elemnt in index one
${array[1]:3:2}
# get length
${#array[@]}
# Loop
for item in "${array[@]}"; do
    echo $item;
done






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


#################
# Brace Expansion (ranges)

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

# Using variables
var=12 echo $(seq 1 $var)


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
# Redirect from string
grep words <<< 'words go here'
# Redirect Special Multiline (it uses the word after `<<` as the delimiter, in this case "EOF")
grep words <<EOF
'words go here'
EOF


# Order Matters!
# stderr -> original_stdout, stdout -> file
echo 2>&1 > filename
# stdout -> file, stderr -> new_stdout -> file
echo > file 2>&1


# ---------------------------
# Process/file substitution
#   creates a pipe, and outputs its location (filepath) as a string
#   Thus allowing the program to pretend to read/write to a file
#
diff <(cmd1) <(cmd1)

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
    # You might need to add `status=none` to avoid pollution of stdout

# Use stdin as a "file"
#   Note: some things accept "-" directly, such as `cat` below
echo text | diff <(cat -) other.txt

# Duplicate output
tee >file | echo 'goes to both file and this command'
# Technically tee will send output to
tee >(cmd1) >file | echo 'cmd1 and original stdout both get here (duplicated output)'
tee >(cmd1) >(cmd2) | echo 'both cmds stdout/stderr goes here'


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
