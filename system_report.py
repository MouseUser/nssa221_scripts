#!/usr/bin/env python3
# Author: Aiden Avery
# Date: 10/3/25

import subprocess

def findNetworkConfig():
    defaultGateway = subprocess.check_output(["ip", "route"], text=True).split()[2]
    fqdn = subprocess.check_output(["hostname"], text=True)
    hostname = fqdn.split(".")[0]
    domain = fqdn.split(".")[1]
    IPInfo = subprocess.check_output(["ifconfig"], text=True).split()
    ipAddress = ""
    netMask = ""
    
    for i in range(0,len(IPInfo)):
        if IPInfo[i] == "inet":
            ipAddress = IPInfo[i+1]
        elif IPInfo[i] == "netmask":
            netMask = IPInfo[i+1]
            break

    DNSInfo = subprocess.check_output(["cat", "/etc/resolv.conf"], text=True).split()
    dns1 = ""
    dns2 = ""
    for j in range(0, len(DNSInfo)):
        if DNSInfo[j] == "nameserver":
            if dns1 == "":
                dns1 = DNSInfo[j+1]
            else:
                dns2 = DNSInfo[j+1]
    
    return defaultGateway, hostname, domain, ipAddress, netMask, dns1, dns2

def findCPUInfo():
    CPUInfo = subprocess.check_output(["cat", "/proc/cpuinfo"], text=True).split(":")
    CPUModel = ""
    processorsNumber = ""
    coresNumber = ""

    for i in range(0, len(CPUInfo)):
        if CPUInfo[i].strip() == "model name":
            CPUModel = CPUInfo[i+1]
        elif CPUInfo[i].strip() == "siblings":
            processorsNumber = CPUInfo[i+1]
        elif CPUInfo[i].strip() == "cpu cores":
            coresNumber = CPUInfo[i+1]
    
    return CPUModel, processorsNumber, coresNumber

def printAndExport():
    date = subprocess.check_output(["date"], text=True)
    print("System Report - " + date)
    defaultGateway, hostname, domain, ipAddress, netmask, dns1, dns2 = findNetworkConfig()
    print("Device Information")
    print("Hostname:\t" + hostname)
    print("Domain:\t" + domain + "\n")
    
    print("Network Information")
    print("IP Address:\t" + ipAddress)
    print("Gateway:\t" + defaultGateway)
    print("Network Mask:\t" + netmask)
    print("DNS1:\t" + dns1)
    print("DNS2:\t" + dns2 + "\n")

    print("Operating System Information")
    print("")

    CPUModel, processorsNumber, coresNumber = findCPUInfo()
    print("Processor Information")
    print("CPU Model:\t" + CPUModel)
    print("Number of processors:\t" + processorsNumber)
    print("Number of cores:\t" + coresNumber)

def main():
    subprocess.run(["clear"])
    printAndExport()

if __name__ == "__main__":
    main()