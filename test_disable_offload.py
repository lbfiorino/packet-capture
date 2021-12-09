import os

iface  = "enp0s3"

os.system("ethtool -K "+iface+" gro on")
os.system("ethtool -K "+iface+" lro on")

