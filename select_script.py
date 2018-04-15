import os,fileinput
import re
import subprocess, sys

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m' 
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

    
def prompt_sudo():
    result = 0
    if os.geteuid() != 0:
        message = "[sudo] password for %u:"
        result = subprocess.check_call("sudo -v -p '%s'" % message, shell=True)
    return result

def banner(color,message):
    print(color+message)

def findVPNfile(): 
    Directory = '/etc/NetworkManager/system-connections/'
    resultList = []

    for root, dirs, files in os.walk(Directory):
        for name in files:
            MatchObj = re.compile(r'.*nordvpn\.com.*')
            result = MatchObj.match(name)
            if result:
                resultList.append(result.group())
    
    return resultList

def getIP(selected):
    MatchObj = re.compile(r'.*tcp')
    result = MatchObj.match(selected)
    if result:
        Directory = '/home/vintux/nordvpn/ovpn_tcp/'
    else:
        Directory = '/home/vintux/nordvpn/ovpn_udp/'
    
    for root, dirs, files in os.walk(Directory):
        for name in files:
            if ( name == selected+".ovpn" ):
                with open(Directory+name) as file:
                    for i,line in enumerate(file):
                        if(i==13):
                            MatchObj = re.compile(r'[0-9]+(?:\.[0-9]+){3}')
                            ip = MatchObj.search(line)
                            return ip.group()

def replaceDispatcher(selected):
    Directory = '/etc/NetworkManager/dispatcher.d/'
    with open(Directory+"vpn-up", "r") as sources:
        lines = sources.readlines()
    with open(Directory+"vpn-up", "w") as sources:
        for line in lines:
            sources.write(re.sub(r'.*nordvpn\.com.*', 'VPN_NAME="'+selected+'"', line))                        
def replaceIPtables(ip):
    MatchObj = re.compile(r'.*tcp')
    protocol = ""
    result = MatchObj.match(selected)
    if result:
        protocol = "tcp"
    else:
        protocol = "udp"
    Filename = '/etc/iptables/iptables.rules'
    with open(Filename,'r') as sources:
        lines = sources.readlines()
    with open(Filename, 'w') as sources:
        for i,line in enumerate(lines):
            if (i==11):
                sources.write('-A OUTPUT -d '+ ip + '/32 -o wlp2s0 -p ' + protocol +' -j ACCEPT\n')
            else:
                sources.write(line)

if __name__ == "__main__":
    if (prompt_sudo() != 0):
        print("Not root, exiting")
        sys.exit(1)
    
    result = findVPNfile()
    banner(BOLD,"WELCOME TO NORDVPN INTERFACE")
    print("\n")
    banner(OKGREEN,"Your installed ovpn files")
    for index, res in enumerate(result):
            message = '[ '+ str(index) + ' ] ' + res;
            banner(HEADER,message)
    
    banner(OKBLUE,"Please select one")
    select = input()
    print("\n")
    print("you selected :")
    selected = result[int(select)]
    banner(OKGREEN,selected)
    
    ip = getIP(selected)
    banner(OKGREEN,ip)
    print("\n")
    replaceDispatcher(selected) 
    replaceIPtables(ip)

    subprocess.Popen(["systemctl","restart","iptables","NetworkManager"],shell = False)
    
