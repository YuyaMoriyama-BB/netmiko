#!/usr/bin/env python
from __future__ import print_function, unicode_literals

# Netmiko is the same as ConnectHandler
from netmiko import Netmiko
from getpass import getpass

my_device = {
    "host": "192.168.1.4",
    "username": "bb",
    "password": "bb",
    "device_type": "nec_ix_os",
}

net_connect = Netmiko(**my_device)

output = net_connect.send_command("show running-config")
print(output)

net_connect.disconnect()