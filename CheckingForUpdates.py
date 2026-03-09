import requests
import json
import os
import sys
import zipfile
import io

GITHUB_RAW_URL = "https://raw.githubusercontent.com/z1ruz-code/IPPulse/main/"
API_RELEASE_URL = "https://api.github.com/repos/z1ruz-code/IPPulse/releases/latest"

def update_from_zip(zip_url):
    try:
        response = requests.get(zip_url, timeout=30)
        response.raise_for_status()
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            members = z.namelist()
            prefix = None
            if members:
                first = members[0]
                if '/' in first:
                    candidate = first[:first.index('/')+1]
                    if all(m.startswith(candidate) for m in members):
                        prefix = candidate
            if prefix is None:
                prefix = ''
            for member in members:
                if member.endswith('/'):
                    continue
                if prefix and member.startswith(prefix):
                    rel_path = member[len(prefix):]
                else:
                    rel_path = member
                dir_name = os.path.dirname(rel_path)
                if dir_name:
                    os.makedirs(dir_name, exist_ok=True)
                with z.open(member) as source, open(rel_path, 'wb') as target:
                    target.write(source.read())
        return True
    except Exception as e:
        print(f"Update error: {e}")
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
        zipball_url = latest_data.get("zipball_url")

        if latest_version and latest_version != current_version and zipball_url:
            print(f"\n[!] Update available: {current_version} -> {latest_version}")
            choice = input("Update now? (y/n): ").lower()
            
            if choice == 'y':
                print("Downloading updates...")
                if update_from_zip(zipball_url):
                    print("UPDATE SUCCESSFUL!")
                    print("Please restart the program (python main.py)")
                    os._exit(0)
                else:
                    print("Error updating files.")
    except Exception as e:
        print(f"Update check error: {e}")

if __name__ == "__main__":
    check_and_update()
