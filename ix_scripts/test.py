#!/usr/bin/env python
from __future__ import print_function, unicode_literals

# Netmiko is the same as ConnectHandler
from netmiko import Netmiko
#from getpass import getpass

my_device = {
    "host": "24bb:bb00:a000:1::1",
    "username": "spgadmbb",
    "password": "spgbitbrain0860bb",
    "device_type": "nec_ix",
}
net_connect = Netmiko(**my_device)

print("=== Pre Check ===")
output = net_connect.send_command("show running-config access-list")
print(output)


print("\n=== Add Config ===")
commands = ["interface Tunnel10.0",
            "ipv6 enable",
            "ipv6 address fd00:a::1/16",
            ]
output = net_connect.send_config_set(commands)
print(output)

print("\n=== Add Config ===")
commands = ["ipv6 access-list test permit icmp echo src any dest any"]

output = net_connect.send_config_set(commands)
print(output)

print("=== Post Check ===")
output = net_connect.send_command("show running-config access-list")
print(output)


net_connect.disconnect()
