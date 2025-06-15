import re
import json
import requests
from bs4 import BeautifulSoup
from utils.request_utils import send_request
from utils.request_utils import random_ua
# from constent.video_api import VideoAPI


def instargam_api(ins_id: str):
    ins_url = []
    type = 0
    request_url = (
        'https://www.instagram.com/graphql/query?variables={"shortcode":"'
        + ins_id
        + '"}&doc_id=8845758582119845&server_timestamps=true'
    )

    response = send_request(url=request_url)
    if not response or response.status_code != 200:
        return None
    result = json.loads(response.text)
    status = result.get("status")
    if status and status == "ok":
        is_video = result.get("is_video")
        result = result.get("data",{}).get("xdt_shortcode_media",{})
        if is_video:
            type = 1
            if result.get("video_url") and result.get("video_url") != "":
                ins_url.append(result.get("video_url"))
        else:
            if result.get("display_url") and result.get("display_url") != "":
                ins_url.append(result.get("display_url"))
            else:
                type = 3
                source = result.get("edge_media_to_tagged_user", {}).get("edges")
                if source:
                    ins_url = [
                        node.get("node", {}).get("display_url") for node in source
                    ]

    return ins_url, type


def parse_snapdownload(url: str):
    ins_url = []
    request_url =  f"https://snapdownloader.com/tools/instagram-downloader/download?url={url}"   
    response = requests.get(request_url)
    html = response.text

    down_div_class = "download-item"
    # 解析 HTML
    soup = BeautifulSoup(html, "html.parser")
    download_items = soup.find_all("div", class_=down_div_class)
    for item in download_items:
        try:
            a_tag = item.find("a")
            if a_tag:
                href = a_tag["href"] if a_tag and a_tag.has_attr("href") else None
                ins_url.append(href)
        except Exception as e:
            print("error")
    return ins_url
