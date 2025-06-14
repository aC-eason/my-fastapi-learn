import json
import traceback
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
from utils.common_utils import get_resolution
from utils.request_utils import random_ua,random_pokopin_headers, random_thepindown_headers   

# 封装请求逻辑，减少重复代码


def make_request(url, headers, data=None, method='GET'):
    try:
        if method == 'POST':
            response = requests.post(url, data=data, headers=headers)
        else:
            response = requests.get(url, headers=headers)
        return response
    except Exception as e:
        print(f"Request to {url} failed: {e}")
        return None


def parse_pokopin(url=None):
    if not url:
        return {}

    base_url = "https://pokopin.com/wp-json/aio-dl/video-data/"
    headers = random_pokopin_headers()
    form_data = {
        'url': url,
        'token': 'f02b4b28b68f0f7d9d3f7d5aecdc798b1defffb4ac963d2fe1624a8a874ce69c'
    }

    response = make_request(base_url, headers, data=form_data, method='POST')
    if response and response.status_code == 200:
        try:
            datas = json.loads(response.text)
            return {
                "title": datas['title'],
                "cover": datas["thumbnail"],
                "quality": datas['medias'][0]['quality'],
                "download": datas['medias'][0]['url'],
                "format": datas['medias'][0]['extension']
            }
        except json.JSONDecodeError:
            print("Error decoding JSON response from Pokopin.")
    return {}


def parse_pinterestdownloader(url=None):
    if not url:
        return {}

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        "user-agent": random_ua()
    }

    request_url = f'https://pinterestdownloader.io/frontendService/DownloaderService?url={url}'
    response = make_request(request_url, headers)
    if response and response.status_code == 200:
        try:
            datas = json.loads(response.text)
            return {
                "title": datas['title'],
                "cover": datas["thumbnail"],
                "quality": datas['medias'][-1]['quality'],
                "download": datas['medias'][-1]['url'],
                "format": datas['medias'][-1]['extension']
            }
        except json.JSONDecodeError:
            print("Error decoding JSON response from Pinterest Downloader.")
    return {}


def parse_thepindown(url=None):
    if not url:
        return {}

    data = {
        'codehap_link': url,
        'codehap': 'true'
    }
    headers = random_thepindown_headers()
    response = make_request(
        'https://thepindown.net/result.php', headers, data=data, method='POST')

    if response:
        try:
            soup = BeautifulSoup(response.text, 'html.parser')
            a_tag = soup.find('a')
            if a_tag and a_tag.get('href'):
                href_value = a_tag.get('href')
                # 解析url中的查询参数
                parsed_url = urlparse(href_value)
                query_params = parse_qs(parsed_url.query)

                # 提取link和type参数
                download_link = query_params.get('link', [None])[0]
                format = query_params.get('type', [None])[0]

            if 'i.pinimg.com' in download_link:
                cover = download_link if format in [
                    'png', 'jpg', 'webp'] else ''
                quality = get_resolution(download_link) if cover else ''

                return {
                    "title": 'Pinterest video',
                    "cover": cover,
                    "quality": quality,
                    "download": download_link,
                    "format": format
                }
        except Exception as e:
            print(f"Error parsing thepindown response: {e}")
    return {}


