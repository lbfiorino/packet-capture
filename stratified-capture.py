import argparse, configparser
import shlex, subprocess
import sys, os, signal, psutil

# Create new process group
os.setpgrp()

current_dir = os.getcwd()

# Parser command-line options
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--interface", dest='iface', help="Network interface.", required=True)
parser.add_argument("-t", "--traffic-type", dest='type', choices=['normal', 'attack', 'all'], help="Traffic type.", required=True)
parser.add_argument("-o", "--out-dir-type", dest='out_dir', help="Directory to save pcap files (defalt: current dir).", default=current_dir)
if len(sys.argv)==1:
     parser.print_help(sys.stderr)
     print("\n")
     exit(1)
args = parser.parse_args()

# Check if network interface exist
if (args.iface not in psutil.net_if_addrs().keys()):
    print("Error: Invalid Network Interface.\n")
    exit(1)

# Check if output dir is writeable
if not os.access(args.out_dir, os.W_OK):
    print("Error: Output dir is not writeable.\n")
    exit(1)    


# Load config with hosts and servers
capture = configparser.ConfigParser()
capture.read("capture.ini")

# Disable NIC Receive Offload
os.system("ethtool -K "+args.iface+" gro off")
os.system("ethtool -K "+args.iface+" lro off")


try: 

    # command = "tcpdump -i "+iface+" -w "+pcap_file+" -U 2> /dev/null"
    # args = shlex.split(command)
    # proc = []
    # proc.append(subprocess.Popen(command, shell=True, executable='/bin/bash'))

    print("Press CTRL+C to exit.")
    while(True):
        input()

finally:
    print("Killing the processes...")
    # Kill all processes in group
    os.killpg(0, signal.SIGKILL)

    # Enable NIC Receive Offload
    os.system("ethtool -K "+args.iface+" gro on")
    os.system("ethtool -K "+args.iface+" lro on")    

    exit()