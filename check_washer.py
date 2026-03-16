import os
import requests
import time

def send_telegram(message):
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        requests.post(url, data={"chat_id": chat_id, "text": message})
    except:
        pass

def check():
    pat_token = os.getenv('LG_PAT_TOKEN')
    headers = {"Authorization": f"Bearer {pat_token}", "Accept": "application/json"}
    
    try:
        # Lấy danh sách thiết bị
        res = requests.get("https://common-api.lge.com/v1/devices", headers=headers, timeout=10)
        devices = res.json().get("result", {}).get("devices", [])
        washer = next((d for d in devices if d['deviceType'] == 'WASHING_MACHINE'), None)
        
        if washer:
            # Lấy trạng thái
            status_url = f"https://common-api.lge.com/v1/devices/{washer['deviceId']}/status"
            res_status = requests.get(status_url, headers=headers, timeout=10)
            data = res_status.json().get("result", {})
            
            # LG trả về phút còn lại (remainTimeMinute)
            remaining = data.get("remainTimeMinute", 0)
            state = data.get("state", "") # Trạng thái máy (RUNNING, STANDBY...)

            print(f"Status: {state}, Remaining: {remaining}m")

            if remaining == 16 and state == "RUNNING":
                send_telegram("🧺 Huy ơi! Đúng 16 phút rồi, ra cho nước xả vào máy giặt nhé!")
                return True # Đã gửi xong, có thể dừng loop
    except Exception as e:
        print(f"Error: {e}")
    return False

# Chạy vòng lặp trong 4 phút 45 giây (để an toàn trước khi workflow tiếp theo bắt đầu)
start_time = time.time()
while time.time() - start_time < 285: 
    sent = check()
    if sent:
        break # Thoát nếu đã thông báo xong
    time.sleep(30) # Kiểm tra mỗi 30 giây