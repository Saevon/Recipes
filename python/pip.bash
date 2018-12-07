

# A lot of things fail due to SSL issues,
LDFLAGS=-L /usr/local/opt/openssl/lib;export CPPFLAGS=-I /usr/local/opt/openssl/include; pip install $PACKAGE


# Special files
# TODO:
# .piprc
# .pypi
