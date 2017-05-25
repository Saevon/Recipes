##############################################
# Mail
#############################################
# postfix
#  https://blog.anupamsg.me/2012/02/14/enabling-postfix-for-outbound-relay-via-gmail-on-os-x-lion-11/


# restart
postfix reload
launchctl stop org.postfix.master
launchctl start org.postfix.master

# logs
tail -f /var/log/mail*

# check the config (-f folds long lines)
postconf
# Show explicitly set values
postconf -n
# show default values
postconf -d

cd /etc/postfix
vim ./main.cf
vim ./aliases
vim ./generic
sudo chmod 600 sasl.passwd
vim sasl.passwd
vim /System/Library/LaunchDaemons/org.postfix.master.plist
launchctl unload -w /System/Library/LaunchDaemons/org.postfix.master.plist
launchctl load -w /System/Library/LaunchDaemons/org.postfix.master.plist


# reload the configs
postfix reload
postmap generic
postmap sasl.passwd

# delete mail
postsuper -d ALL
# delete deferred mail
postsuper -d deferred

# view queue
postqueue -p
# Retry all mail
postqueue -f




#####################
# Config info

# Launchd
Socket: opens up sockets to be listened on by the launchd system (and directed to the daemon, starting it up)

WatchPaths: List of Paths or Directories, if anything appears here your script is launched
QueueDirectories: Same but only Directories



# Permitted connections
smtpd_recipient_restrictions=
    check_recipient_access hash:/etc/postfix/filtered_domains # Looks at /etc/postfix/filtered_domains to see rules for allowed recipients
    permit_mynetworks # Enables any networks listed in mynetworks to send
    permit_sasl_authenticated # Enables anyone who authenticates through sasl
# Enable the given addresses to send mail
mynetworks = 127.0.0.0/8, [::1]/128, 10.172.249.186

# The interfaces to listen on: (this needs postfix to be stopped then started. NOT reloaded)
inet_interfaces = 10.172.249.186
inet_interfaces = loopback-only
inet_interfaces = all

# Directory to store mail. This should match the launchd one above
queue_directory = /private/var/spool/postfix
