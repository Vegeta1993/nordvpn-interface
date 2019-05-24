#!/bin/sh

#
# Disable ufw and reset all rules to defaults
#
sudo ufw disable
sudo ufw reset

#
# Set the default rules to deny everything
#
sudo ufw default deny incoming
sudo ufw default deny outgoing

#
# Allow in/out on the local private network
#
sudo ufw allow in to 192.168.1.0/24
sudo ufw allow out to 192.168.1.0/24

#
# Allow traffic out on the VPN tunnel adapter (tun0)
#
sudo ufw allow out on tun0 from any to any

#
# Allow UDP traffic out to the VPN server so VPN client can connect
#
sudo ufw allow out to 185.180.12.56 port 443 proto tcp

#
# Enable ufw. Try to hit anything. It should fail while the VPN is down.
#
sudo ufw enable
