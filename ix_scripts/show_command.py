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

output = net_connect.send_command("show running-config")
print(output)

net_connect.disconnect()
