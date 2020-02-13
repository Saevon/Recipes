# Networking

# Figure out Mac OSX DNS servers
scutil --dns

# See nameservers (some)
/etc/resolv.conf

# Get a DNS entry
dig $hostname
dig @$nameserver
dig +trace $hostname



# ------------------------------------------------------------------------------
# See all open ports on machine
# without sudo this only shows your processes
# -i makes this do network operations

# Grab all connections for TCP
sudo lsof -i TCP
# Grab all connections for TCP in a particular state
sudo lsof -i TCP -s TCP:LISTEN
# Grab all connections to a specific port
sudo lsof -i :8080


# ------------------------------------------------------------------------------
# Routing & Interfaces

# Add an route to an interface
sudo ifconfig lo0 alias
# Remove a route for an interface
sudo ifconfig lo0 -alias

# Check routing tables
netstat -nr
arp -a

# See `ip neigbour` man page for states
# ARP state   meaning
# permanent   never expires; won't be verified
# noarp       normal expiration; won't be verified
# reachable   normal expiration
# stale       still usable; needs verification            Suspicious, please run verify
# delay       schedule ARP request; needs verification    TBD
# probe       sending ARP request                         In-Progress
# incomplete  first ARP request sent                      some requests for this ip are awaiting resolution
# failed      no response received                        Retry-count reached, verification failed, etc

# Check active connections
netstat

# Tun/TAP Interfaces: Interface over SSH
# https://backreference.org/2010/03/26/tuntap-interface-tutorial/



# ------------------------------------------------------------------------------
# Admin  Work

# Get top process using network
nethogs
# Examine traffic by interface / source
iftop

# See how a packet travels
traceroute
# See better breakdown of which link is causing slowness
mtr

# Process
top
htop



# ------------------------------------------------------------------------------
# SSL



# View Certificate

# For most extensions
openssl x509 -in cert.{pem,cer,crt} -text -noout
# If you get 'unable to load certificate' its probably an encoding issue, try DER
openssl x509 -in cert.der -inform der -text -noout

# See ssl.sh for more info






# Convert Certificate Types

# PEM to DER
openssl x509 -in ${IN}.pem -inform pem -outform der -out ${OUT}.der
# DER to PEM
openssl x509 -in ${IN}.der -inform der -outform pem -out ${OUT}.pem
