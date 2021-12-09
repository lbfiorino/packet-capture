#!/usr/bin/python3

import shlex, subprocess
import time, os, psutil, signal

os.setpgrp() # create new process group, become its leader

#argument = '...'
#proc = subprocess.Popen(['python', 'bar.py', argument], shell=True)
#time.sleep(3) # <-- There's no time.wait, but time.sleep.
#pid = proc.pid # <--- access `pid` attribute to get the pid of the child process.

#command = "tcpdump -i enp0s3 -w teste.pcap -U"
command = "tcpdump -i enp0s3 -w teste.pcap -U 2> /dev/null"

args = shlex.split(command)

print(args)
proc = subprocess.Popen(command, shell=True, executable='/bin/bash')

pid = proc.pid
print(pid)

#process = psutil.Process(pid)

#print(process.cmdline())

input()

#os.system(f"pkill -P {pid}")

os.killpg(0, signal.SIGKILL) # kill all processes in my group

exit(0)

