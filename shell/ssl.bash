# --------------------------------------------------------------------------------------
# Certificate Authority (CA)
# https://superuser.com/questions/738612/openssl-ca-keyusage-extension

# Creating our root PRIVATE Key
openssl genrsa -out saevon.root.key 4096
    # Add this if you want to encrypt the key as well (with a passphrase)
    -des3


# Create our ROOT Certificate
openssl req -x509 -new -key saevon.root.key -sha256 -days 365 -out saevon.root.crt
    # You need to explicitly choose to encrypt (or not)
    -nodes
    # OR
    -des3

# Sign people's Certificates (send back the *.crt)
openssl req -x509 -in mydomain.com.csr -CA saevon.root.crt -CAkey saevon.root.key
    -out mydomain.com.crt -config ssl.conf.ini
    # Every certificate you sign needs a unique serial number... this is stored on a file
    # You will need one of the following:

    # The first time you create a serial (indicating how many things you've signed)
    -CAcreateserial
        # it creates a file with the same name as the *.crt except *.srl

    # Every time afterwards, just supply this file
    -CAserial saevon.root.srl

# Verify that something was signed by you
openssl verify -CAfile saevon.root.crt mydomain.com.crt


# MacOSX Splitting from Keychain.app (after exporting)
openssl pkcs12 -in path.p12 -out newfile.crt.pem -clcerts -nokeys
openssl pkcs12 -in path.p12 -out newfile.key.pem -nocerts -nodes


# --------------------------------------------------------------------------------------
# Server SSL




# TODO:
# 1) Create this system once
# 2) Verify that extensions (e.g. the SAN[second name] get copied over when you sign the crt)
# 3) Theres also EV (Extended Validation) in case you want the green lock symbol
# https://gist.github.com/Soarez/9688998

# --------------------------------------------------------------------------------------
# Server SSL

# Create our Server Certificate PRIVATE KEY
openssl genrsa -out mydomain.com.key 2048

# Certificate Signing Request (csr)
#   Ask a Root CA to sign your SSL Certificate
openssl req -new -key mydomain.com.key -out mydomain.com.csr -config mydomain.com.conf
    # You can also add in other things... such as a SAN: (extra domain names)

# Now Get the CA to actually sign it
#    csr >> crt
# The CSR is useless after wards
rm mydomain.com.csr

# OR self-sign it
#   Note you need the INI again to get extensions working properly...???
openssl x509 -req -days 365 -in mydomain.com.csr -signkey mydomain.com.key -out mydomain.com.crt  -extfile mydomain.com.ini




# Getting information out of a .crt
openssl x509 -text -noout -in mydomain.com.crt

# Checking a servers certificate
#   You might need
openssl s_client -connect server.com:443
    # Optionally you can specify a root CA to use, a bundle
    # OR you can use an intermediate cert (especially if the server doesn't provide it)
    -CAfile certificate.bundle.pem







# --------------------------------------------------------------------------------------
# Double check permissions (and location)
sudo chmod u=rw,g=r,o=   /etc/ssl/private/*.key
     chown root:ssl-cert
sudo chmod u=rw,g=r,o=r /etc/ssl/cert/*.crt
     chown root:ssl-cert





# Notes:
*.pem # A Jumble of things: CSR, CRT, KEY, etc
*.p12 # A Jumble of Certificate + Private Key (CRT + KEY) (MacOSX)
*.crt # A certificate PEM file (but apps know its a certificate)
*.csr # Basically your public key for the CA to issue a certificate
*.srl # A Serial identifier for a CA


# Don't forget about wildcard certificates (locking down all subdomains)
*.saevon.ca
# Which won't actually match the base(naked) domain... so include them both
