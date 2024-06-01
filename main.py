import speedtest
import datetime
import time
from concurrent.futures import ThreadPoolExecutor

INTERVAL_SEC = 60

st = speedtest.Speedtest()
st.get_best_server()


def get_timestamp():
    date = datetime.datetime.now()
    return date.isoformat()


def speed_test():
    download_speed = st.download() / 1024 / 1024  # Mbpsに変換
    upload_speed = st.upload() / 1024 / 1024  # Mbpsに変換
    ping = st.results.ping

    return download_speed, upload_speed, ping


def send_data(download_speed, upload_speed, ping):
    print(f"Download Speed: {download_speed:.2f} Mbps")
    print(f"Upload Speed: {upload_speed:.2f} Mbps")
    print(f"Ping: {ping} ms")


def task():
    download_speed, upload_speed, ping = speed_test()
    timestamp = get_timestamp()

    print(f"Timestamp: {timestamp}")

    send_data(download_speed, upload_speed, ping)


def main():
    with ThreadPoolExecutor(max_workers=2, thread_name_prefix="thread") as executor:
        while True:
            print("--- Start Speed Test ---")
            executor.submit(task)
            time.sleep(INTERVAL_SEC)


main()
