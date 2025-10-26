#!/usr/bin/env python3
# Author: Aiden Avery
# Date: 10/26/25

import pathlib, subprocess

HOME_DIR = pathlib.Path.home()

def findFile(dir, fileName):
    # searches entire system for file while redirecting errors to /dev/null
    result = subprocess.run(f"sudo find {dir} -name '{fileName}'", stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True, text=True)
    
    if result.returncode != 0 and result.returncode != 1:
        return "False"
    else:
        return result.stdout

def createSymLink():
    fileName = ""
    result = ""
    while True:
        print("Enter the file name to create a symbolic link for:")
        fileName = input()
        result = findFile("/", fileName)
        if result == "False":
            print("File not found. Check correct spelling.\n")
        else:
            break

    splitFiles = result.split()
    if len(splitFiles) > 1:
        print(f"Multiple files with the name '{fileName}' were found:\n")
        for i in range(len(splitFiles)):
            print(f"{i+1}. {splitFiles[i]}")

        print(f"\nPlease select the file you want to create a shortcut for (1-{len(splitFiles)}):")
        while True:
            chosenFile = int(input())
            if chosenFile < 1 or chosenFile > len(splitFiles):
                print("Invalid input. Please select a listed number.")
            else:
                break

        result = splitFiles[chosenFile-1]

    subprocess.run(f"ln -s {result} {HOME_DIR}/Desktop/{fileName}", shell=True)

def deleteSymLink():
    print("Enter the name of the symlink to delete:")

    result = ""
    while True:
        fileName = input()
        result = findFile(f"{HOME_DIR}/Desktop/", fileName)
        if result == "False":
            print("Symlink not found. Check your spelling.")
        else:
            break
    
    subprocess.run(f"rm {result}", shell=True)

def generateReport():
    print("\nSymlink Report:\n")
    currentDir = subprocess.check_output("pwd", text=True)
    print("Current directory: " + currentDir + "\n")
    
    symLinks = subprocess.check_output(f'ls -al {HOME_DIR}/Desktop | grep "^l"', shell=True, text=True).strip().split("\n")

    print(f"The number of links is {len(symLinks)}.\n")
    
    if (len(symLinks) > 0):
        print("Symbolic Link\tTarget Path")
        for i in range(0, len(symLinks)):
            symLinksSplit = symLinks[i].split(" ")
            for j in range(0, len(symLinksSplit)):
                if symLinksSplit[j] == "->":
                    print(f"{symLinksSplit[j-1]} -> {symLinksSplit[j+1]}")

    print("\nTo return the menu, press Enter...")
    input()

def main():
    subprocess.run(["clear"])

    while True:
        print("\nSelect an option from the following list:")
        print("1. Create symbolic link")
        print("2. Delete symbolic link")
        print("3. Generate symbolic link report")
        print("4. Quit\n")
    
        userInput = input()
        if userInput == "1":
            createSymLink()
        elif userInput == "2":
            deleteSymLink()
        elif userInput == "3":
            generateReport()
        elif userInput == "4":
            print("Exiting script...")
            break
        else:
            print("Invalid input. Please enter a listed number.")

if __name__ == "__main__":
    main()