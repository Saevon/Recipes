########################################
# Vim
########################################

# If this returns -clipboard, you can't copy to clipboard
# (registers @ or + )
vim --version | grep '+clipboard'

# exit vim with an error code (e.g. during git commit to abort)
:cq
