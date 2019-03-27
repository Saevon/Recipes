# Automating telnet requests
expect -c '
set timeout 10

# Creates the process to listen to
spawn telnet myserver.com 80

# Waits for specific data
expect "Connected to"

# Now send the actual request
# (\r represents newlines)
send "GET / HTTP/1.1\r"
send "Host: 127.0.0.1\r"
send "\r"
send "\r"

# Wait for response
expect eof
'


# Telnet
telnet $server $port
    # Opens up a telnet prompt (See Above)

# SSL telnet: (-quiet hides cert info)
openssl s_client -connect -quiet $server:$port
    # Opens up a telnet prompt (See Above)


# HTTP Headers
Authorization: Basic base-64-encoded-auth=======
