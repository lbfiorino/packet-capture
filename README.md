# packet-capture

# Disable GRO/LRO on Linux

```bash
# Show NIC Features
ethtool -k <interface>
# Show only offload
show-features
ethtool --show-offload <interface>

# Disable/Enable generic-receive-offload
ethtool -K <dev> gro on|off

# Disable/Enable large-receive-offload
ethtool -K <dev> lro on|off
```
