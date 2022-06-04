import time
import datetime

import requests

# 从网络上获取标准北京时间。
def get_beijin_time():
    try:
        url = 'https://beijing-time.org/'
        request_result = requests.get(url=url)
        if request_result.status_code == 200:
            headers = request_result.headers
            net_date = headers.get("date")
            gmt_time = time.strptime(net_date[5:25], "%d %b %Y %H:%M:%S")
            bj_timestamp = int(time.mktime(gmt_time) + 8 * 60 * 60)
            return datetime.datetime.fromtimestamp(bj_timestamp)
    except Exception as exc:
        # return datetime.datetime.now()
        return datetime.datetime(2099, 6, 14, 00, 00, 00)

if __name__ == "__main__":
    print(get_beijin_time());