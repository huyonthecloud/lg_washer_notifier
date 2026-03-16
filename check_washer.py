import os
import requests

def send_telegram(message):
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, data={"chat_id": chat_id, "text": message})

def main():
    pat_token = os.getenv('LG_PAT_TOKEN')
    headers = {"Authorization": f"Bearer {pat_token}", "Accept": "application/json"}
    
    # 1. Lấy danh sách thiết bị
    try:
        res = requests.get("https://common-api.lge.com/v1/devices", headers=headers)
        devices = res.json().get("result", {}).get("devices", [])
        washer = next((d for d in devices if d['deviceType'] == 'WASHING_MACHINE'), None)
        
        if washer:
            # 2. Lấy trạng thái máy giặt
            status_url = f"https://common-api.lge.com/v1/devices/{washer['deviceId']}/status"
            res_status = requests.get(status_url, headers=headers)
            remaining = res_status.json().get("result", {}).get("remainTimeMinute", 0)
            
            print(f"Thời gian còn lại: {remaining} phút")
            
            # 3. Kiểm tra mốc 16 phút (hoặc trong khoảng 15-17 để trừ hao độ trễ của GitHub)
            if remaining == 19:
                send_telegram("🧺 Huy ơi! Còn đúng 16 phút, ra cho nước xả vào nhé!")
    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == "__main__":
    main()