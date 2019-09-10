# (Don't run this stuff...)
exit 0



# ------------------------------------------------------------------------------
# Truncate
tr -d 'a-z'
tr -d '\n\r\t '
tr -d '[:space:]'

# Swap
#   Warning! it only works on individual chars (not sequences)
tr 'a-z' 'A-Z'
tr ' ' '\t'
# Rot13
tr 'a-zA-Z' 'n-za-mN-ZA-M'

# Remove repeating Chars
tr -s '0-9'



# Force Terminal notification (Ping)
tput bel


# ------------------------------------------------------------------------------

# Error messages
2>&1 echo "ERROR: blah"

# Escapes
printf "hey!\n  indented newlines?\n"
echo -e '\033'






# ------------------------------------------------------------------------------
# Search

# Inverted
grep -v 'text'
