# NORDVPN-INTERFACE

Nordvpn doesn't have any application for linux to quickly change between vpn servers. So I have created a python script which will help with this. This is just a command line tool and needs other files like *iptables-rules*, *vpn-up* and *passwd* file. Python program doesn't need any other external libraries.

## iptables-rules
This contains rules for iptables. Here I allow only outgoing connections to server IP and internal IP's. All other outgoing connections are dropped except on DNS requests.

## passwd 
This file has to contain your nordvpn username and password.

## vpn-up
This file will work with nm-openvpn to automatically connect to vpn when connecting to a server. 

## select_script
This will give us a banner and list all installed openvpn files from NetworkManager. Once user selects the remote VPN server, it reads IP address from the nordvpn .ovpn file and replace iptable and dispatcher files. In the end, restart both networkManager and iptables. 

This does not take care of ipv6 leak and dns leak. For DNS leak, I have set my resolver to nordvpn DNS server and changed its attributes. For ipv6 leak, I have disables ipv6. 

You can check your network status on [ipleak.net](https://ipleak.net)
