#!/usr/bin/python3

import argparse, configparser
import shlex, subprocess
import sys, os, signal, psutil


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# This script must be run as root!
if not os.geteuid()==0:
    sys.exit('This script must be run as root!')


# Get working directory
current_dir = os.getcwd()


# Parser command-line options
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--interface", dest='iface', help="Network interface.", required=True)
parser.add_argument("-t", "--traffic-type", dest='traffic_type', choices=['normal', 'attack', 'all'], help="Traffic type.", required=True)
parser.add_argument("-o", "--out-dir-type", dest='out_dir', help="Directory to save pcap files (defalt: current dir).", default=current_dir)
if len(sys.argv)==1:
     parser.print_help(sys.stderr)
     print("\n")
     exit(1)
args = parser.parse_args()


# Create new process group to kill all process in group
os.setpgrp()
# Processes
proc = []

# Load hosts and servers
captureConfig = configparser.ConfigParser()
captureConfig.read("capture.ini")


# Function to start the captures
def start_capture(section):
    for t in captureConfig['target']:
        target_ip_port = captureConfig['target'][t].split(':')
        for h in captureConfig[section]:
            host_ip = captureConfig[section][h]
            sep = "_port"
            pcapfile = host_ip+"_to_"+sep.join(target_ip_port)+"_"+captureConfig['capture']['proto']+"_"+section+".pcap"
            CMD = "tcpdump -U -n -i "+args.iface+" -w "+pcapfile+" 'host "+target_ip_port[0]+" and host "+host_ip
            if (captureConfig['capture']['proto']):
                CMD += " and "+captureConfig['capture']['proto']
                if (len(target_ip_port) == 2): 
                    CMD += " port "+target_ip_port[1]         
            
            CMD += "' 2> /dev/null"
        
            print(CMD)
            # Start tcpdump
            #proc.append(subprocess.Popen(CMD, shell=True, executable='/bin/bash'))


# Check if network interface exist
if (args.iface not in psutil.net_if_addrs().keys()):
    print("Error: Invalid Network Interface.\n")
    exit(1)


# Check if output dir is writeable
if not os.access(args.out_dir, os.W_OK):
    print("Error: Output dir is not writeable.\n")
    exit(1)    


# Disable NIC Receive Offload
os.system("ethtool -K "+args.iface+" gro off lro off tso off gso off ufo off")

try: 
    if (args.traffic_type == "all"):
        start_capture("attack")
        start_capture("normal")
    else:
        start_capture(args.traffic_type)

    print("\n")
    print(bcolors.HEADER + "--> Capturing on "+args.iface+"." + bcolors.ENDC)
    print("\nPress CTRL+C to exit.\n")
    while(True):
        input()

finally:
    
    print(bcolors.WARNING + "Killing the processes..." + bcolors.ENDC)
    # Kill all processes in group
    os.killpg(0, signal.SIGKILL)

    # Enable NIC Receive Offload
    os.system("ethtool -K "+args.iface+" gro on lro on tso on gso on ufo on")   

    exit()