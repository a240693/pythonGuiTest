import time
import datetime
import random
import requests


# 从网络上获取标准北京时间。
def get_def():
    try:
        url = 'https://api.pcrdfans.com/x/v1/search'
        defJson = {
            # "切噜~蹦巴噼啪唎巴啵啪切拉噼嘭切巴啵巴巴切巴啵拉噼巴巴切唎唎噼切"
            "_sign": "切噜~蹦巴噼啪唎巴啵啪切拉噼嘭切巴啵巴巴切巴啵拉噼巴巴切唎唎噼切" ,
            "def": [
                108501
            ],
            "language": 0,
            "nonce": "szemow0l6p9cizkj",
            "page": 1,
            "region": 2,
            "sort": 1,
            "ts": 1655437631
        }
        request_result = requests.post(url=url, json=defJson)
        return request_result.text

    except Exception as exc:
        # return datetime.datetime.now()
        print(exc)
        return datetime.datetime(2099, 6, 14, 00, 00, 00)

def another():
    try:
        url = 'https://api.pcrdfans.com/x/v1/search'
        defJson = {
            "_sign": "切噜~哔蹦啪铃拉蹦唎铃切哔叮啰啪蹦唎蹦蹦啪叮嘭哔叮蹦蹦啪拉拉切啪",
            "def": [
                105201
            ],
            "language": 0,
            "nonce": "mc84kcljjj1nac8f",
            "page": 1,
            "region": 2,
            "sort": 1,
            "ts": 1655439819
        }
        request_result = requests.post(url=url, json=defJson)
        return request_result.text

    except Exception as exc:
        # return datetime.datetime.now()
        print(exc)
        return datetime.datetime(2099, 6, 14, 00, 00, 00)


def generateNonce():
    firstNum = random.random()
    print(firstNum)
    secondNum = firstNum.__format__(36)
    print(secondNum)
    # return random.random().toString(36).substring(2, 10) + random.random().toString(36).substring(2, 10);
    return secondNum

def teamViewerTest():
    url = 'https://login.teamviewer.com/UserManagement/UpdateProfile'
    dataJson = {
        "CommentAfterSessionEnd": "false",
        "CustomQJConfigId": None,
        "CustomQSConfigId": None,
        "EnableSessionCodeEmails": "true",
        "DisplayName": "YLX-PC",
        "Email": "461605470@qq.com",
        "LogConnections": "false",
        "WantsProductPreview": "false",
        "EmailLanguage": 0,
        "WantsTrustDeviceViaPush": "false"
    }
    request_result = requests.post(url=url, json=dataJson)
    return request_result.text

if __name__ == "__main__":
    # generateNonce()
    print(teamViewerTest())
    # print(generateNonce())
