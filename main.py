import speedtest
import datetime
import time
import requests
import os
import sys
from urllib.parse import urljoin
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor

load_dotenv(".env", verbose=True)

INTERVAL_SEC = 10

st = speedtest.Speedtest()
st.get_best_server("211.1.206.2")

arg_type = [arg for arg in sys.argv if arg.startswith("type:")]
if len(arg_type) == 1:
    splited_arg = arg_type[0].split(":")
    network_type = splited_arg[1]
else:
    print("network type が指定されていません")
    print("  ex) python main.py type:5g")
    sys.exit(1)


def get_timestamp():
    date = datetime.datetime.now()
    return date.isoformat()


def speed_test():
    download_speed = st.download() / 1024 / 1024  # Mbpsに変換
    upload_speed = st.upload() / 1024 / 1024  # Mbpsに変換
    ping = st.results.ping

    return download_speed, upload_speed, ping


def send_data(timestamp, download_speed, upload_speed, ping):
    base_url = os.environ.get("API_URL")
    url = urljoin(base_url, f"/api/network/{network_type}")
    send_data = [
        {
            "time": timestamp,
            "down": download_speed,
            "up": upload_speed,
            "ping": ping,
        }
    ]

    try:
        res = requests.post(
            url,
            json=send_data,
        )
        print("--- API Response ---")
        print(res.status_code)
        print(res.json())
    except requests.exceptions.RequestException as e:
        print(e)


def task():
    download_speed, upload_speed, ping = speed_test()
    timestamp = get_timestamp()

    print("--- Speed Test Result ---")
    print(f"Timestamp: {timestamp}")
    print(f"Download Speed: {download_speed:.2f} Mbps")
    print(f"Upload Speed: {upload_speed:.2f} Mbps")
    print(f"Ping: {ping} ms")
    send_data(timestamp, download_speed, upload_speed, ping)


def main():
    with ThreadPoolExecutor(max_workers=2, thread_name_prefix="thread") as executor:
        while True:
            print("--- Start Speed Test ---")
            executor.submit(task)
            time.sleep(INTERVAL_SEC)


main()
