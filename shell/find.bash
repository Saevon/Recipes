# (Don't run this stuff...)
exit 0



# Filename match
#   Warning! use quotes or else the shell will do the expansion instead
find . -name "*.pdf"
ack -g 'filename'

# Logic
find . ! -name "*.pdf"
find . -name "*.pdf" -or -name "*.pdf"
find . \( -name "*.png" -or -name "*.jpg" \) -user saevon



# Ownership
find . -user saevon
find . -group staff


# Type
find . -type f
find . -type d
find . -type l   # Sym Link
find . -type p   #Pipe (FIFO)
find . -type s   # Socket


# Map a command on files
#    (echoes the file, then the file without the pdf extension)
find . -name "*.pdf" -exec sh -c 'echo $0, ${0%.pdf}' {} \

# Filter files passing command
#  (Finds files that only have ASCII chars)
find . -exec sh -c "file '{}' | grep ASCII" \;

# Filter by size
#   Warning!  if you don't use a suffix it means "filesystem-blocks" (usually 512 bytes)
find . -size -2000c +1000c
find . -size 5002b


