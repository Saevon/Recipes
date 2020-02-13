# A lot of things fail due to SSL issues,
LDFLAGS=-L /usr/local/opt/openssl/lib;export CPPFLAGS=-I /usr/local/opt/openssl/include; pip install $PACKAGE

# Install package from local-cache
pip download $PACKAGE
    # Download to a specific directory instead of "./"
    --dest $CACHE_DIR
    # Skip dependencies
    --no-dep
pip install $PACKAGE
    --find-links=file:///home/user/$MY_FULL_PATH
    --no-index --index-url=file:///dev/null


# Special files
# TODO:
# .piprc
# .pypi

