#!/usr/bin/env python3
# Author: Aiden Avery
# Date: 9/10/25

import subprocess

REMOTE_ADDRESS = "www.google.com"
DNS_ADDRESS = "129.21.3.17" # RIT's DNS server
DEFAULT_GATEWAY = subprocess.check_output(["ip", "route"], text=True).split()[2]

def displayMenu():
    print("Select an option from the following list:")
    print("1. Display the default gateway")
    print("2. Test local connectivity")
    print("3. Test remote connectivity")
    print("4. Test DNS resolution")
    print("5. Exit/quit the script")
    print()

def displayGateway():
    print("Default gateway: " + DEFAULT_GATEWAY)

def testConnectivity(address):
    print("Testing connectivity ...")
    print("Pinging " + address + " ...")
    try:
        consoleOutput = subprocess.check_output(["ping", address, "-c", "1"], text=True)
        pingResult = consoleOutput.split("\n")
        if pingResult[1].split()[0] == "64": # checks for returned ping
            print("Ping succeeded!")
        else:
            print("Ping failed.")
    except subprocess.CalledProcessError:
        print("Ping failed.")

def testDNS():
    print("Testing DNS ...")
    consoleOutput = subprocess.check_output(["nslookup", REMOTE_ADDRESS], text=True)
    lookupResult = consoleOutput.split("\n")
    if lookupResult[3] == "Non-authoritative answer:": # checks if DNS server recognizes address
        print("DNS lookup succeeded!")
    else:
        print("DNS lookup failed.")

def main():
    chosenOption = ""
    subprocess.run(["clear"])
    while chosenOption != "5":
        displayMenu()
        chosenOption = input()
        if chosenOption == "1":
            displayGateway()
        elif chosenOption == "2":
            testConnectivity(DNS_ADDRESS)
        elif chosenOption == "3":
            testConnectivity(REMOTE_ADDRESS)
        elif chosenOption == "4":
            testDNS()
        elif chosenOption == "5":
            print("Exiting script ...")
        else:
            print("Invalid input. Please input a number for selection.")

if __name__ == "__main__":
    main()