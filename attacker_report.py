#!/usr/bin/env python3
# Author: Aiden Avery
# Date: 11/6/25

from geoip import geolite2
import re, subprocess, datetime

IP_REGEX = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'

def countFailedAttempts(filename):
    ipCounts = dict()
    try:
        with open(filename) as file:
            for line in file:
                match = re.search(IP_REGEX, line)
                if match is not None:   
                    if match.group(0) not in ipCounts.keys(): ipCounts[match.group(0)] = 1  #check if IP address was already logged
                    else: ipCounts[match.group(0)] += 1
        
        return ipCounts
    except FileNotFoundError:
        print("File not found.")
        return 0;

def main():
    subprocess.run("clear")
    report = countFailedAttempts("/home/student/syslog.log")
    if report == 0:
        return 0;
    
    ipList = sorted(report, key=report.get) #sort list by attempts in ascending order
    ipList = [ip for ip in ipList if report[ip] >= 10] #only include addresses with 10 or more attempts

    date = datetime.datetime.now().strftime("%B %d, %Y")
    print(f"Attacker Report - {date}\n")

    print("COUNT\tIP ADDRESS\tCOUNTRY")
    for ip in ipList:
        ipLookup = geolite2.lookup(ip)
        country = ""
        if ipLookup is not None: country = ipLookup.country
        print(f"{report[ip]}\t{ip}\t{country}")

if __name__ == "__main__":
    main()