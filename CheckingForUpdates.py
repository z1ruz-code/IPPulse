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
            print(f"\n[!] Доступно обновление: {current_version} -> {latest_version}")
            choice = input("Обновить программу и перезапустить? (y/n): ").lower()
            
            if choice == 'y':
                print("Загрузка актуальных компонентов...")
                
                files_to_update = ["main.py", "CheckingForUpdates.py", "config.json"]
                
                success = True
                for file in files_to_update:
                    if not update_file(file):
                        success = False
                
                if success:
                    print("Обновление завершено успешно.")
                    print("Запуск новой версии в отдельном окне...")

                    if os.name == 'nt':
                        subprocess.Popen(['start', 'cmd', '/k', 'python', 'main.py'], shell=True)
                    else:
                        os.execv(sys.executable, [sys.executable] + sys.argv)
                    
                    sys.exit()
                else:
                    print("Ошибка при обновлении некоторых файлов.")
    except Exception:
        pass
