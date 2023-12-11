#!/usr/bin/env python
from __future__ import print_function, unicode_literals

# Netmiko is the same as ConnectHandler
from netmiko import Netmiko
#from getpass import getpass

my_device = {
    "host": "24bb:bb00:a000:1::1",
    "username": "spgadmbb",
    "password": "spgbitbrain0860bb",
    "device_type": "nec_ix_os",
}

net_connect = Netmiko(**my_device)

net_connect.config_mode()

print("=== Pre Check ===")
output = net_connect.send_command("show running-config interface Tunnel10.0")
print(output)


print("\n=== Add Config ===")
commands = ["interface Tunnel10.0",
            "ipv6 enable",
            "ipv6 address fd00:a::1/16",
            "configure"]
output = net_connect.send_config_set(commands)
print(output)

print("=== Post Check ===")
output = net_connect.send_command("show running-config interface Tunnel10.0")
print(output)


net_connect.disconnect()
