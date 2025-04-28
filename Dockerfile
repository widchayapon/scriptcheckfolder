# ใช้ Python เวอร์ชันล่าสุด
FROM python:3.10

# ตั้ง working directory ใน container
WORKDIR /app

# คัดลอกไฟล์ไปยัง container
COPY monitor_nfs.py .
COPY .env .

# ติดตั้งไลบรารีที่ต้องใช้
RUN pip install psutil requests python-dotenv

# รันโปรแกรม
CMD ["python", "monitor_nfs.py"]
