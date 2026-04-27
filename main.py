import requests
import json
import os
import sys
import time
import ipaddress
import CheckingForUpdates

def is_valid_ip(ip_str: str) -> bool:
    try:
        ipaddress.ip_address(ip_str)
        return True
    except ValueError:
        return False

def main():
    CheckingForUpdates.check_and_update()

    print("IPPulse by z1ruz-code")

    ip_address = input("Введите IP-адрес: ").strip()
    if not is_valid_ip(ip_address):
        print("Некорректный IP-адрес. Введите правильный IPv4 или IPv6 адрес.")
        time.sleep(1)
        sys.exit(1)

    else:
        url = f"https://api.ipapi.is/?q={ip_address}"

        response = requests.get(url)
        data = response.json()

        if "company" in data and "whois" in data["company"]:
            del data["company"]["whois"]
        if "asn" in data and "whois" in data["asn"]:
            del data["asn"]["whois"]

        json_output = json.dumps(data, indent=4, ensure_ascii=False)
        for line in json_output.splitlines():
            print(line)
            time.sleep(0.01)

        save = input("\nСохранить результат в .txt? (y/n): ").lower()
        if save == "y":
            folder = "reports"
            os.makedirs(folder, exist_ok=True)
            filepath = os.path.join(folder, f"{ip_address}.txt")
            with open(filepath, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            print(f"Отчёт сохранён: {filepath}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем.")
        sys.exit(0)
