# Networking

# See nameservers (some)
/etc/resolv.conf
# MAC
scutil --dns

# Get a DNS entry
dig $hostname
dig @$nameserver
dig +trace $hostname
# nslookup is deprecated

# Follow DNS search your system uses (Including Caches)
# MAC
dscacheutil -q host -a name $hostname
# Linux
getent hosts $hostname




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
# SSL



# View Certificate

# For most extensions
openssl x509 -in cert.{pem,cer,crt} -text -noout
# If you get 'unable to load certificate' its probably an encoding issue, try DER
openssl x509 -in cert.der -inform der -text -noout






# Convert Certificate Types

# PEM to DER
openssl x509 -in ${IN}.pem -inform pem -outform der -out ${OUT}.der
# DER to PEM
openssl x509 -in ${IN}.der -inform der -outform pem -out ${OUT}.pem
