#!/usr/bin/env python3

import fnmatch
import os
import shutil
import winreg
import json
import sys
import subprocess

# Example launch command: python cleanUp.py -s -p config.json

# Load config file
try:
    # Get config file path
    # There needs to be -p "path" in the launch command
    if "-p" in sys.argv:
        configPath = sys.argv[sys.argv.index("-p") + 1]
    else:
        configPath = "config.json"
        
    with open(configPath) as f:
        config = json.load(f)
except FileNotFoundError:
    print("Error: Config file not found")
    sys.exit(1)
except json.JSONDecodeError:
    print("Error: Invalid config file")
    sys.exit(1)

skipPrompts = False

# Get launch arguments
if len(sys.argv) > 1:
    # If has -s argument, skip prompts
    if "-s" in sys.argv:
        skipPrompts = True

# Stop services
if not skipPrompts:
    prompt = input("Do you want to stop services? (y/n) ")
else:
    prompt = 'y'

if prompt.lower() == 'y':
    print("Stopping services...")
    for service in config["services"]:
        try:
            print(f"Stopping {service}...")
            subprocess.call(["net", "stop", service], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"{service} stopped.")
        except subprocess.CalledProcessError:
            print(f"Error: Failed to stop {service}")
else:
    print("Skipping service stop.")

# Stop executables
if not skipPrompts:
    prompt = input("Do you want to stop executables? (y/n) ")
else:
    prompt = 'y'

if prompt.lower() == 'y':
    print("Stopping executables...")
    for executable in config["executables"]:
        # Add .exe to the end of the executable if it doesn't already have it
        if not executable.endswith(".exe"):
            executable += ".exe"
            
        try:
            print(f"Stopping {executable}...")
            subprocess.call(["taskkill", "/f", "/im", executable], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"{executable} stopped.")
        except subprocess.CalledProcessError:
            print(f"Error: Failed to stop {executable}")
else:
    print("Skipping executable stop.")

# Delete files
if not skipPrompts:
    prompt = input("Do you want to delete files? (y/n) ")
else:
    prompt = 'n' # Don't delete files by default

if prompt.lower() == 'y':
    print("Scanning for files to delete...")
    files_to_delete = []

    for file in config["files"]:
        item = file["item"]
        type = file.get("type", "")

        if "%" in item:
            item = os.path.expandvars(item)
        
        # If item contains a wildcard or mutiple onens ("item": "*.tmp;*.log;") then get all files that match the wildcard
        if type == "WILDCARD":
            # Split the item string into a list of wildcards
            wildcards = item.split(";")
            for wildcard in wildcards:
                for root, dirs, files in os.walk("C:/"):
                    for name in files:
                        if fnmatch.fnmatch(name, wildcard):
                            files_to_delete.append(os.path.join(root, name))

        # Remove all files in the directory but not the directory itself
        elif type == "RECURSE":
            # Get all files and folders in the directory
            for root, dirs, files in os.walk(item):
                # Remove all files and folders in the directory

                # Remove all files in the directory
                for name in files:
                    files_to_delete.append(os.path.join(root, name))
                
                # Remove all subdirectories in the directory
                for name in dirs:
                    files_to_delete.append(os.path.join(root, name))
        
        # Remove all files in the directory and the directory itself
        elif type == "REMOVESELF":
            # Remove the directory itself
            files_to_delete.append(item)
        else:
            files_to_delete.append(item)

    # Replace / with \ in paths
    files_to_delete = [file.replace("/", "\\") for file in files_to_delete]
    # Remove duplicates
    files_to_delete = list(dict.fromkeys(files_to_delete))

    print("The following files will be deleted:")
    for file in files_to_delete:
        print(file)

    # Confirm with the user before deleting the items
    confirm = input("Are you sure you want to delete these items? (y/n) ")

    # clear the console
    print("\033c", end="")

    if confirm.lower() == 'y':
        for file in files_to_delete:
            try:
                if os.path.isdir(file):
                        shutil.rmtree(file)
                else:
                    os.remove(file)
            except FileNotFoundError:
                print(f"Error: {file} not found")
            except PermissionError:
                print(f"Error: Permission denied for {file}")

        print("Items successfully deleted.")
    else:
        print("Delete operation cancelled.")
else:
    print("Skipping file delete.")

# Delete registry keys
if not skipPrompts:
    prompt = input("Do you want to delete registry keys? (y/n) ")
else:
    prompt = 'y'

if prompt.lower() == 'y':
    print("Deleting registry keys...")

    # Delete registry keys in the list (e.g. "regKeys": ["HKEY_CURRENT_USER\Software\\Microsoft\\Windows\\CurrentVersion\\Run"])
    for element in config["regKeys"]:

        # from HKEY_CURRENT_USER\Software\... get HKEY_CURRENT_USER and Software\...
        splittedThing = element.split("\\", 1)

        regKey = splittedThing[0]
        key = splittedThing[1]

        # If regKey is not HKEY_CURRENT_USER it is not safe to delete
        if regKey != "HKEY_CURRENT_USER":
            print(f"Error: {element} is not a safe key to delete")
            continue

        print(f"Deleting {key}...")

        # Connect to the registry
        reg = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        try:
            winreg.DeleteKey(reg, key)
        except WindowsError as e:
            if e.winerror != 2:
                print(f"Error: {e}")
else:
    print("Skipping registry key delete.")

# Clean event logs
if not skipPrompts:
    prompt = input("Do you want to clean event logs? (y/n) ")
else:
    prompt = 'y'

if prompt.lower() == 'y':
    print("Cleaning event logs...")
    try:
        subprocess.call(["wevtutil", "clear-log", "Application"])
        subprocess.call(["wevtutil", "clear-log", "System"])
        subprocess.call(["wevtutil", "clear-log", "Security"])
    except subprocess.CalledProcessError:
        print("Error: Failed to clean event logs")
else:
    print("Skipping event log cleaning.")
    
# Restart PC
if not skipPrompts:
    prompt = input("Do you want to restart the PC? (y/n) ")
else:
    prompt = 'n'
    
if prompt.lower() == 'y':
    try:
        subprocess.call(["shutdown", "/r", "/t", "0"])
    except subprocess.CalledProcessError:
        print("Error: Failed to restart PC")
else:
    print("Skipping PC restart.")