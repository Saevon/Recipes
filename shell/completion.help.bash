


# Completing many words, you can list them as a space separated array before
# WARNING! don't forget the space prefix when doing +=
local actions
actions=""
actions+=" branches heads"
actions+=" current history show"


# Multiple completions can be mixed together
COMPREPLY = ( $(compgen -f -- "$cur"; compgen -d -S / -- "$cur") )

# You can also Add a filter
# The filter is inversed however, anything matched is normally REMOVED
# JUST add the ! to flip it back
$(compgen -A file -X '!*.ini' -- ${cur}) )
