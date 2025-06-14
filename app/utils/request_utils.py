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

def random_thepindown_headers():
    headers = {
        'accept': '*/*',
        'accept-language': 'en,zh-CN;q=0.9,zh;q=0.8,ru;q=0.7',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie': 'codehap_domain=thepindown.net; cfzs_google-analytics_v4=%7B%22ndwV_pageviewCounter%22%3A%7B%22v%22%3A%221%22%7D%7D; __gads=ID=d2ee7a0e0ce83b50:T=1737531447:RT=1737531447:S=ALNI_MboPvXtB4lbmEg9UIeWc5BCH2JfKQ; __gpi=UID=00000fd3342a0c1e:T=1737531447:RT=1737531447:S=ALNI_Maf3R7SrWn9XpYShSI4QSab1grNBw; __eoi=ID=27fde07f7e7a72c4:T=1737531447:RT=1737531447:S=AA-AfjbHSp8pzRHYxfzmCCO2kE-H; FCNEC=%5B%5B%22AKsRol-k0whJGUf_9gW_wXTmBeECzxZ3yZHEYgmBm3-4i5LF12ak_-WxvM664DFvXs81lNlBg5Ks3S6K5AU2rsIccWaghK_mYIQ-VyJCrLvPaBUhoe5q_pumQn_DWE0r_4ntqnbEZPG_sUrnE65TUgVEwXuEANPSiA%3D%3D%22%5D%5D; cfz_google-analytics_v4=%7B%22ndwV_engagementDuration%22%3A%7B%22v%22%3A%220%22%2C%22e%22%3A1769067610660%7D%2C%22ndwV_engagementStart%22%3A%7B%22v%22%3A1737531612157%2C%22e%22%3A1769067612554%7D%2C%22ndwV_counter%22%3A%7B%22v%22%3A%225%22%2C%22e%22%3A1769067610660%7D%2C%22ndwV_ga4sid%22%3A%7B%22v%22%3A%22731965745%22%2C%22e%22%3A1737533410660%7D%2C%22ndwV_session_counter%22%3A%7B%22v%22%3A%221%22%2C%22e%22%3A1769067610660%7D%2C%22ndwV_ga4%22%3A%7B%22v%22%3A%2295c528b2-55b9-466b-bad6-c331ae8fe8ea%22%2C%22e%22%3A1769067610660%7D%2C%22ndwV__z_ga_audiences%22%3A%7B%22v%22%3A%2295c528b2-55b9-466b-bad6-c331ae8fe8ea%22%2C%22e%22%3A1769067443938%7D%2C%22ndwV_let%22%3A%7B%22v%22%3A%221737531610660%22%2C%22e%22%3A1769067610660%7D%7D',
        'origin': 'https://thepindown.net',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://thepindown.net/',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }
    first_num = random.randint(121, 132)
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

    headers['user-agent'] = ua
    headers['sec-ch-ua'] = '"Not A(Brand";v="8", "Chromium";v="{}", "Google Chrome";v="{}"'.format(
        first_num, first_num)
    return headers


def random_pokopin_headers():
    headers = {
        'accept': '*/*',
        'accept-language': 'en,zh-CN;q=0.9,zh;q=0.8,ru;q=0.7',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': (
            'pll_language=en; PHPSESSID=grpom2ncrg6ld9vp6f4fcc08bl; '
            'cf_clearance=3Y0A.iuDBbr3KKLM6ZCKOxk18G7E1PyZFUB22ViOkQA-1737528927-1.2.1.1-'
            '0Vm1v5orMRzTgJaYDXrjJue_b5Ef.uYSQDyiLyNdp84E.pbpQAOiNhhrxZfF9h5CBOQzML9rJDLX3Gy41czj.GWIDCn8bZV5vN6PfBSiJQwnvIjEYt_5b5vrJxLrVo.K80UuuGNUMflnUoNZWXQuXPmUqfIsx5yzMaKg2pAKBNjsNoqfJl9yTvIKNxAW_DxhgTnygjRcNgbQJbdw0ElhyDTkZEmnL5Q9fXbdO.NnuKxmil1xMKZ9CRK8nsU24KHeZwceH8lm7eevqNlZbFgoHYXe3Lz3K4GtCKYoF_gCXMU; _ga_EFZ491EWK8=GS1.1.1737528928.1.0.1737528928.0.0.0; _ga=GA1.1.918652346.1737528929'
        ),
        'origin': 'https://pokopin.com',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://pokopin.com/',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    }

    first_num = random.randint(121, 132)
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

    headers['user-agent'] = ua
    headers['sec-ch-ua'] = '"Not A(Brand";v="8", "Chromium";v="{}", "Google Chrome";v="{}"'.format(
        first_num, first_num)
    return headers



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
