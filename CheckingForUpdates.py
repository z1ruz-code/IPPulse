import requests
import json
import os
import sys
import subprocess

GITHUB_RAW_URL = "https://raw.githubusercontent.com/z1ruz-code/IPPulse/main/"
API_RELEASE_URL = "https://api.github.com/repos/z1ruz-code/IPPulse/releases/latest"

def update_file(filename):
    try:
        response = requests.get(GITHUB_RAW_URL + filename, timeout=10)
        response.raise_for_status()
        with open(filename, "wb") as f:
            f.write(response.content)
        return True
    except Exception:
        return False

def check_and_update():
    try:
        if os.path.exists("config.json"):
            with open("config.json", "r") as f:
                config = json.load(f)
        else:
            config = {"version": "0.0.0"}
            
        current_version = config.get("version", "0.0.0")

        response = requests.get(API_RELEASE_URL, timeout=5)
        response.raise_for_status()
        latest_data = response.json()
        latest_version = latest_data.get("tag_name", "").lstrip('v')

        if latest_version and latest_version != current_version:
            print(f"\n[!] Update available: {current_version} -> {latest_version}")
            choice = input("Update and restart? (y/n): ").lower()
            
            if choice == 'y':
                print("Downloading updates...")
                
                files_to_update = ["main.py", "CheckingForUpdates.py", "config.json"]
                
                success = True
                for file in files_to_update:
                    if not update_file(file):
                        success = False
                
                if success:
                    print("Update successful.")
                    print("Restarting in a new window...")

                    if os.name == 'nt':
                        subprocess.Popen('start cmd /k "python main.py"', shell=True, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
                    else:
                        os.execv(sys.executable, [sys.executable] + sys.argv)
                    
                    os._exit(0)
                else:
                    print("Error updating files.")
    except Exception:
        pass
