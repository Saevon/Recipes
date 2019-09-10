#!/bin/bash
# (Don't run this stuff...)
exit 0


# Style:
# http://redsymbol.net/articles/unofficial-bash-strict-mode/
# https://jvns.ca/blog/2017/03/26/bash-quirks/
# https://jonlabelle.com/snippets/view/markdown/defensive-bash-programming
# http://mywiki.wooledge.org/BashGuide/Practices

# Common bashisms
# http://mywiki.wooledge.org/BashFAQ
# http://tldp.org/LDP/abs/html/

# Shell Practice
# https://cmdchallenge.com/#/corrupted_text



# Useful flags
    # Abort on failure
    set -e
    # Abort on unset variables
    set -u
    # If a glob fails to expand, error out (instead of leaving the *)
    shopt -s failglob
    # Abort if any pipe command fails
    #    Warning! this makes handling with $? harder
    set -o pipefail

    # Make sure bash doesn't treat spaces as word boundaries
    #  Keeps loops & such from breaking "spaced sentences"
    IFS=$'\n\t'



    # Debugging: prints all commands its going to run
    set -x


# Testing return values
    # Good for handling `set -e`
    # Will be unset on pass
    local retval=0;
    grep ... || retval=$?


# Main Function
    function main() (
        # statements

        return 0;
    )


    # If run directly call main
    [[ "$0" == "$BASH_SOURCE" ]] && main "$@"


# Getting Script path
    PROG_DIR=`( readlink -f "${BASH_SOURCE[0]}" || greadlink -f "${BASH_SOURCE[0]}" ) 2>/dev/null`


# Cleanup
    function cleanup() (
      # Your cleanup code here
      echo 1;
    )
    trap cleanup EXIT SIGINT SIGTERM


# Argument parsing
    usage () {
        2>&1 cat <<-EOF
		Usage: ${0} [-h] [-v]

		This program does something

		---------------------------
		Parameters (ENV Variables)

			WITH_FLAG   Enables something

		---------------------------
		Options

			-h, --help        Shows the Usage
			-v, --verbose     Verbose Mode

		EOF
    }

    # Rough, needs fixing
    # got this idea from here:
    # http://kirk.webfinish.com/2009/10/bash-shell-script-to-use-getopts-with-gnu-style-long-positional-parameters/
    local arg=
    for arg; do
        local delim=""
        case "$arg" in
            #translate --gnu-long-options to -g (short options)
            --user)           args="${args}-c ";;
            --help)           args="${args}-h ";;
            --verbose)        args="${args}-v ";;
            #pass through anything else
            *) [[ "${arg:0:1}" == "-" ]] || delim="\""
                args="${args}${delim}${arg}${delim} ";;
        esac
    done

    # Overwrite the internal options variable
    set -- ${args}

    # Parse the options
    while getopts "vuh:" opt; do
        case ${opt} in
         v) readonly IS_VERBOSE=1 ;;
         u) local user=$OPTARG;;
         h) 2>&1 usage; exit 0;;
         :) 2>&1 echo "Required argument for -${opt} "; exit 2;;
         ?) 2>&1 echo "Unknown arg: -$opt"; exit 2;;
        esac
    done

    # Validate the options
    if [ -z "${user+unset}" ]; then
        2>&1 echo "User is required"
    fi

    # Usually this would be in a cmdline helper function


# Crash rebooting
    function main() (
        echo 'started'

        # OH NO Crashed...
        return 1;
    )

    # Keep retrying if we get an error return
    # DO NOT retry on signals (e.g. SIGINT)
    function keep_alive() (
        main || keep_alive;
    )


# Bash Typing
    # Declare integer
    declare -i val
    # Declare Array
    declare -a list

    # Declare readonly
    declare -r var

    # Export variable
    declare -x var
