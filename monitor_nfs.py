import os
import requests
import time
from dotenv import load_dotenv

# โหลดค่า ENV
load_dotenv()
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# ตั้งค่าการแจ้งเตือน
STORAGE_FREE_LIMIT_BYTES = int(os.getenv("STORAGE_FREE_LIMIT_BYTES")) * 1024 * 1024
CHECK_INTERVAL = 10  # วินาที
STORAGE_PATH = "/home/file_test"  # โฟลเดอร์ที่ต้องการเช็คพื้นที่

def send_discord_alert(message):
    """ ส่งแจ้งเตือนเข้า Discord Webhook """
    data = {"content": message}
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    if response.status_code == 204:
        print("✅ แจ้งเตือนสำเร็จ!")
    else:
        print(f"⚠️ ส่งแจ้งเตือนล้มเหลว: {response.status_code}")
def get_folder_size(path):
    """ คำนวณขนาดรวมของไฟล์ในโฟลเดอร์ """
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if os.path.isfile(file_path):  # ตรวจสอบว่าเป็นไฟล์
                total_size += os.path.getsize(file_path)
    return total_size

def monitor_system():
    """มอนิเตอร์ Storage: เช็กทีละโฟลเดอร์ย่อย และแจ้งเตือนถ้ามีขนาดเกิน 200MB"""
    while True:
        if not os.path.exists(STORAGE_PATH):
            print(f"❌ ไม่พบโฟลเดอร์ {STORAGE_PATH}")
            time.sleep(CHECK_INTERVAL)
            continue

        subfolders = [os.path.join(STORAGE_PATH, name) for name in os.listdir(STORAGE_PATH) if os.path.isdir(os.path.join(STORAGE_PATH, name))]
        
        folder_count = len(subfolders)
        send_discord_alert(f"📦 พบโฟลเดอร์ทั้งหมด {folder_count} อันใน '{STORAGE_PATH}'")

        for folder in subfolders:
            folder_size = get_folder_size(folder)
            folder_size_mb = folder_size / (1024 * 1024)

            print(f"[INFO] ขนาดโฟลเดอร์ '{folder}': {folder_size_mb:.2f} MB")

            if folder_size >= STORAGE_FREE_LIMIT_BYTES:
                # ถ้าเกิน 200MB -> แจ้งเตือน
                send_discord_alert("⚠️ รายงานจากเครื่อง NFS")
                send_discord_alert(
                    f"⚠️ โฟลเดอร์ '{folder}' มีขนาดไฟล์ทั้งหมด {folder_size_mb:.2f} MB ({folder_size} Bytes) ซึ่งเกิน 200 MB!"
                )
            else:
                # ถ้าไม่เกิน 200MB -> แจ้งปกติ
                send_discord_alert(
                    f"✅ โฟลเดอร์ '{folder}' มีขนาด {folder_size_mb:.2f} MB ปกติ"
                )

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    monitor_system()
