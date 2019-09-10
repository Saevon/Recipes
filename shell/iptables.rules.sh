#!/usr/bin/env iptables
# shellcheck disable
*filter

# Defaults
-P INPUT   DROP
-P FORWARD ACCEPT
-P OUTPUT  ACCEPT

# Accepts all established inbound connections
-A INPUT  -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
-A OUTPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT


# Drop bad packets
-A INPUT   -m conntrack --ctstate INVALID -j DROP
-A FORWARD -m conntrack --ctstate INVALID -j DROP
-A OUTPUT  -m conntrack --ctstate INVALID -j DROP


# Allows all loopback (lo0) traffic
-A INPUT -i lo -j ACCEPT
-A OUTPUT -o lo -j ACCEPT

# Drop all traffic to 127/8 that doesn't use lo0
-A INPUT ! -i lo -d 127.0.0.0/8 -j REJECT
-A OUTPUT ! -o lo -d 127.0.0.0/8 -j REJECT


# ---------------------------------------
# Attacks

# flooding of RST packets, smurf attack Rejection
-A INPUT -p tcp -m tcp --tcp-flags RST RST -m limit --limit 2/second --limit-burst 2 -j ACCEPT

# Protecting portscans
# Attacking IP will be locked for 24 hours (3600 x 24 = 86400 Seconds)
-A INPUT -m recent --name portscan --rcheck --seconds 86400 -j DROP
-A FORWARD -m recent --name portscan --rcheck --seconds 86400 -j DROP

# Remove attacking IP after 24 hours
-A INPUT -m recent --name portscan --remove
-A FORWARD -m recent --name portscan --remove

# These rules add scanners to the portscan list, and log the attempt.
# Use the unused port 140 as a port scan sign
-A INPUT -p tcp -m tcp --dport 140 -m recent --name portscan --set -j LOG --log-prefix "[iptables] PORTSCAN: "
-A INPUT -p tcp -m tcp --dport 140 -m recent --name portscan --set -j DROP

-A FORWARD -p tcp -m tcp --dport 140 -m recent --name portscan --set -j LOG --log-prefix "[iptables] PORTSCANE: "
-A FORWARD -p tcp -m tcp --dport 140 -m recent --name portscan --set -j DROP






# ---------------------------------------
# Services

# Allows HTTP and HTTPS connections from anywhere (the normal ports for websites)
-A INPUT -p tcp --dport 80 -j ACCEPT
-A INPUT -p tcp --dport 443 -j ACCEPT

# Allow DNS Connections (Externally)
-A INPUT -p tcp --dport 53 -j ACCEPT
-A INPUT -p udp --dport 53 -j ACCEPT


# Allows SSH connections
-A INPUT -p tcp -m conntrack --ctstate NEW --dport 22 -j ACCEPT


# Limit ping requests
-A INPUT -p icmp -m icmp --icmp-type echo-request -m limit --limit 10/second -j ACCEPT


# Accept Misc Internal Network connections
-A INPUT -s 10.0.0.10/24 -j ACCEPT


# ----------------------------------------
COMMIT
