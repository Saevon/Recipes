import os
import platform
import socket



def is_ipv4_address(address):
    ''' Whether this is a valid ipv4 address '''
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:
        # inet_pton is not available on all platforms
        # (but its more accurate)
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        # Technically 'incomplete' ipv4 addresses work for inet_aton
        #    10.0
        #    10
        #  ETC, it just pads them with zeroes... but we only accept full addresses
        return address.count('.') == 3
    except socket.error:
        return False

    return True


def is_ipv6_address(address):
    ''' Whether this is a valid ipv6 address (but not ipv4) '''
    try:
        socket.inet_pton(socket.AF_INET6, address)
    except AttributeError:
        return False
        # Function doesn't exist... in which case we cannot tell
    except socket.error:
        # It is not an ipv6 address
        return False
    return True


def get_hostname():
    '''
    Tries to figure out the hostname for the machine

    It will try and get a human readable name as best it can
    But might end up returning an IP address if it fails
    '''

    # ------------------------------------------------------------
    # Try 1:

    hostname = platform.node()
    if not hostname:
        # This returns empty string if it failed
        hostname = None

    # ------------------------------------------------------------
    # Try 2: Sometimes we have the env variable set
    #    Though cron, or system launched commands often DO NOT

    if hostname is None:
        hostname = os.getenv('HOSTNAME', None)

    # ------------------------------------------------------------
    # Try 3: Windows might set this custom variable
    #    Note: on systems where "socket" is not available this is the best bet
    #    TODO: make the socket import optional for those cases
    if hostname is None:
        hostname = os.getenv('COMPUTERNAME')

    # ------------------------------------------------------------
    # Try 4: This is usually the recommended one
    #    should succeed if nothing else did
    if hostname is None:
        hostname = socket.gethostname()

    # ------------------------------------------------------------
    # Now we should have a hostname...

    # If we get an IP try and translate it
    if is_ipv4_address(hostname) or is_ipv6_address(hostname):
        try:
            hostname = socket.gethostbyaddr(socket.gethostname())[0]
        except socket.herror:
            # We failed... keep the IP name then
            pass

    return hostname






print(is_ipv4_address('10.0.0.1'))

# TODO: Add edge cases for "ipv4/ipv6" addresses












