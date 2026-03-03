import time
import subprocess

ADB_TARGET = "192.168.18.174:5555"

def connect_adb():
    print("Connecting to ADB")
    subprocess.run(["adb", "connecT", ADB_TARGET], check=False)
    
def run_scraper():
    print("Uruchamiam scraper")
    subprocess.run(["python", "appium_automation.py"], check=False)

while True:
    connect_adb()
    run_scraper()
    print("Sleep 600s")
    time.sleep(600)
