

# Create SSH filesystem
#   Logs into the server, mounting its path unto yours (and syncing them)
sshfs -o defer_permissions user@hostname.com:/${PATH} ${MOUNT}
    # To Undo the mount...
    unmount ${MOUNT}


# -------------------------------------------------------------------
# SSH Keys

# generate private key from public key
ssh-keygen -y -f id_rsa -C "serghei@Windy" > id_rsa.pub


# -------------------------------------------------------------------
# SSH Tunneling


# Creating a public ssh tunnel (anyone can login to the target machine)

    # The ssh server creating the tunnel needs an option set
    #     /etc/sshd/config
    # Needed to bind to 0.0.0.0 (otherwise it silently goes to localhost)
    #    @intermediary
    GatewayPorts yes

    # Create the a tunnel back to yourself from some server
    ssh -R 0.0.0.0:22333:localhost:22 $INTERMEDIARY

    # Use the Tunnel
    #    @client
    ssh $INTERMEDIARY -p22333

# Creating an SSH Tunnel through a client you cannot control
# (Also safer, due to the login requirements)

    # IF you cannot allow * binding
    # (1) Create a "login only" binding
    #     @server
    ssh -R :22333:localhost:22 -N $SERVER
    # (2) Create a tunnel from your client (with login)
    #     @Client
    ssh -R :22222:localhost:22333 -N $SERVER

    # Use the tunnel
    #    @client
    ssh localhost -p22222

