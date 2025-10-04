#!/usr/bin/env python3
# Author: Aiden Avery
# Date: 10/3/25

import subprocess
from types import MemberDescriptorType

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
    CPUInfo = subprocess.check_output(["cat", "/proc/cpuinfo"], text=True).split("\n")
    CPUModel = ""
    processorsNumber = ""
    coresNumber = ""

    for i in range(0, len(CPUInfo)):
        splitLine = CPUInfo[i].split(":")
        if splitLine[0].strip() == "model name":
            CPUModel = splitLine[1].strip()
        elif splitLine[0].strip() == "siblings":
            processorsNumber = splitLine[1].strip()
        elif splitLine[0].strip() == "cpu cores":
            coresNumber = splitLine[1].strip()
    
    return CPUModel, processorsNumber, coresNumber

def findOSInfo():
    OSInfo = subprocess.check_output(["cat", "/etc/os-release"], text=True).split("\n")
    OSName = ""
    OSVersion = ""
    kernelVersion = subprocess.check_output(["uname", "-r"], text=True)

    for i in range(0, len(OSInfo)):
        splitLine = OSInfo[i].split("=")
        if splitLine[0] == "PRETTY_NAME":
            OSName = splitLine[1].strip('"')
        elif splitLine[0] == "VERSION_ID":
            OSVersion = splitLine[1].strip('"')
    
    return OSName, OSVersion, kernelVersion

def findStorageInfo():
    storageInfo = subprocess.check_output(["df"], text=True).split()
    totalStorage = ""
    usedStorage = ""
    freeStorage = ""

    for i in range(0, len(storageInfo)):
        if storageInfo[i].strip() == "/":
            freeStorage = storageInfo[i-2]
            usedStorage = storageInfo[i-3]
            break
    
    totalStorage = str((int(usedStorage) + int(freeStorage))/1073742) + " GiB"
    usedStorage = str(int(usedStorage)/1073742) + " GiB"
    freeStorage = str(int(freeStorage)/1073742) + " GiB"

    return totalStorage, usedStorage, freeStorage

def findMemoryInfo():
    memoryInfo = subprocess.check_output(["free"], text=True).split()
    totalRAM = ""
    availableRAM = ""

    for i in range(0, len(memoryInfo)):
        if memoryInfo[i].strip() == "Mem:":
            totalRAM = memoryInfo[i+1]
            availableRAM = memoryInfo[i+3]
            break
    
    totalRAM = str(int(totalRAM)/1073742) + " GiB"
    availableRAM = str(int(availableRAM)/1073742) + " GiB"

    return totalRAM, availableRAM

def generateList():
    date = subprocess.check_output(["date"], text=True)
    fileContents = []
    fileContents.append("System Report - " + date)
    defaultGateway, hostname, domain, ipAddress, netmask, dns1, dns2 = findNetworkConfig()
    fileContents.append("Device Information")
    fileContents.append("Hostname:        " + hostname)
    fileContents.append("Domain:          " + domain + "\n")
    
    fileContents.append("Network Information")
    fileContents.append("IP Address:      " + ipAddress)
    fileContents.append("Gateway:         " + defaultGateway)
    fileContents.append("Network Mask:    " + netmask)
    fileContents.append("DNS1:            " + dns1)
    fileContents.append("DNS2:            " + dns2 + "\n")

    OSName, OSVersion, kernelVersion = findOSInfo()
    fileContents.append("Operating System Information")
    fileContents.append("Operating System: " + OSName)
    fileContents.append("OS Version:      " + OSVersion)
    fileContents.append("Kernel Version:  " + kernelVersion + "\n")

    totalStorage, usedStorage, freeStorage = findStorageInfo()
    fileContents.append("Storage Information")
    fileContents.append("System Drive Total: " + totalStorage)
    fileContents.append("System Drive Used: " + usedStorage)
    fileContents.append("System Drive Free: " + freeStorage + "\n")

    CPUModel, processorsNumber, coresNumber = findCPUInfo()
    fileContents.append("Processor Information")
    fileContents.append("CPU Model:       " + CPUModel)
    fileContents.append("Number of processors: " + processorsNumber)
    fileContents.append("Number of cores: " + coresNumber + "\n")

    totalRAM, availableRAM = findMemoryInfo()
    fileContents.append("Memory Information")
    fileContents.append("Total RAM:       " + totalRAM)
    fileContents.append("Available RAM:   " + availableRAM + "\n")

    return fileContents

def main():
    subprocess.run(["clear"])
    fileContents = generateList()
    filePath = "/home/" + subprocess.check_output(["whoami"], text=True) + "/" + subprocess.check_output(["hostname"], text=True).split(".")[0] + "_system_report.log"

    file = open(filePath, "w")
    for line in fileContents:
        print(line)
        file.write(line + "\n")

if __name__ == "__main__":
    main()
