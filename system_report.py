#!/usr/bin/env python3
# Author: Aiden Avery
# Date: 10/3/25

def findNetworkConfig():
    defaultGateway = subprocess.check_output(["ip", "route"], text=True).split()[2]
    