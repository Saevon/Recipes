########################################
# Commit Hashes
###

# Where you currently are
HEAD
@
# One commit back
HEAD~1
# First Parent (Branch code was merged into, or just parent)
HEAD^
HEAD^1
# Second Parent (Merged in Branch)
HEAD^2

# Commit Range
origin/master..1c3618
HEAD~1..HEAD
# XOR Range (disjunctive union)
refA...refB

# Negative Range
# No commits that are reachable by refA
git log --not refA refB refC
git log ^refA refB refC

