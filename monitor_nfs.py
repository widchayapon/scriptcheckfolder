import os
import requests
import time
from dotenv import load_dotenv

# โหลดค่า ENV
load_dotenv()
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# ตั้งค่าการแจ้งเตือน
STORAGE_FREE_LIMIT_BYTES = 200 * 1024 * 1024  # 200 MB
CHECK_INTERVAL = 5  # วินาที
STORAGE_PATH = "/home/file_test"  # โฟลเดอร์ที่ต้องการเช็คพื้นที่

def send_discord_alert(message):
    """ ส่งแจ้งเตือนเข้า Discord Webhook """
    data = {"content": message}
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    if response.status_code == 204:
        print("✅ แจ้งเตือนสำเร็จ!")
    else:
        print(f"⚠️ ส่งแจ้งเตือนล้มเหลว: {response.status_code}")

def test_discord_connection():
    """ ทดสอบการเชื่อมต่อกับ Discord Webhook """
    test_message = "✅ ระบบ Monitor พร้อมทำงาน! จากเครื่อง 14"
    data = {"content": test_message}
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)

    if response.status_code == 204:
        print("✅ เชื่อมต่อกับ Discord Webhook สำเร็จ!")
    else:
        print(f"⚠️ ไม่สามารถเชื่อมต่อกับ Discord Webhook: {response.status_code}")

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
    """ มอนิเตอร์ Storage: แจ้งเตือนถ้าพื้นที่เหลือน้อยกว่า 200 MB """
    test_discord_connection()  # เช็กการเชื่อมต่อก่อนเริ่ม Monitor

    while True:
        folder_size = get_folder_size(STORAGE_PATH)
        folder_size_mb = folder_size / (1024 * 1024)  # แปลงเป็น MB

        # แสดงขนาดของไฟล์รวมในโฟลเดอร์
        print(f"[INFO] ขนาดทั้งหมดของไฟล์ใน {STORAGE_PATH}: {folder_size_mb:.2f} MB")

        # เช็คถ้าขนาดทั้งหมดของไฟล์ในโฟลเดอร์มีขนาดเกิน 200 MB
        if folder_size >= STORAGE_FREE_LIMIT_BYTES:
            send_discord_alert("⚠️ รายงานจากเครื่อง NFS")
            send_discord_alert(
                f"⚠️ Storage '{STORAGE_PATH}' มีขนาดไฟล์ทั้งหมด {folder_size_mb:.2f} MB ({folder_size} Bytes) ซึ่งเกิน 200 MB!"
            )

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    monitor_system()
