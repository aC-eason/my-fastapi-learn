import requests
import random


def random_ua():
    """
    生成随机user-agent
    """
    first_num = random.randint(55, 76)
    third_num = random.randint(0, 3800)
    fourth_num = random.randint(0, 140)
    os_type = [
        '(Windows NT 6.1; WOW64)', '(Windows NT 10.0; WOW64)',
        '(Macintosh; Intel Mac OS X 10_14_5)'
    ]
    chrome_version = 'Chrome/{}.0.{}.{}'.format(
        first_num, third_num, fourth_num)

    ua = ' '.join(['Mozilla/5.0', random.choice(os_type), 'AppleWebKit/537.36',
                   '(KHTML, like Gecko)', chrome_version, 'Safari/537.36']
                  )
    return ua


def send_request(url:str, method='GET', headers=None,data= None):
    if not headers:
        {
            "Content-Type": "application/json",
            "User-Agent": random_ua(),
        }
    try:
        if method == 'POST':
            response = requests.post(url, data=data, headers=headers)
        else:
            response = requests.get(url, headers=headers)
        return response
    except Exception as e:
        print(f"Request to {url} failed: {e}")
        return None
