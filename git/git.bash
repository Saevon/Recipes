


# Choosing merge resolutions

# Force git to accept one side
--strategy-option ours
--strategy-option theirs

# Short form:
-X ours
-X theirs



merge --abort
cherry-pick --abort
rebase --abort

commit
cherry-pick --continue
rebase --continue

rebase --skip



function detectStatus() {
    isRebase = $( [ -z $(ls $(git rev-parse --git-dir) | grep rebase-merge    ) ]; echo $?)
    isCherry = $( [ -z $(ls $(git rev-parse --git-dir) | grep CHERRY_PICK_HEAD) ]; echo $?)
    isMerge  = $( [ -z $(ls $(git rev-parse --git-dir) | grep MERGE_HEAD      ) ]; echo $?)

    if [ "$( expr $isRebase + $isMerge + $isCherry )" -gt 1 ]; then
        echo "Can't detect state";
    fi
}

