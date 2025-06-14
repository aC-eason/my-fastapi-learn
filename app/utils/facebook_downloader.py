import re
import json
from utils.request_utils import send_request
from utils.request_utils import random_ua
from model.pydantic_model.facebook_source_model import FacebookSource


def parse_tools360(url):
    request_url = (
        "https://tools360.net/tool-assets/downloader-tools/php/fbvideo_downloader.php?url="
        + url
    )
    headers = {
        "User-Agent": random_ua(),
    }
    fb_source_data = None
    response = send_request(request_url, headers=headers)
    if not response or response.status_code != 200:
        return fb_source_data

    result = json.loads(response.text)
    title = result.get("title", "")
    video_download_link = result.get("links", {})
    hd_video = video_download_link.get("Download High Quality", "")
    sd_video = video_download_link.get("Download Low Quality", "")
    if hd_video and sd_video and title:
        fb_source_data = FacebookSource(
            title=title, hd_video_url=hd_video, sd_video_url=sd_video
        )

    return fb_source_data


def parse_getfb(url):
    request_url = "https://apiv2.getfb.net/Facebook/DetectVideoInfo"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": random_ua(),
    }
    payload = json.dumps(
        {
            "html": "",
            "id": "",
            "videoId": url,
        }
    )
    fb_source_data = None
    response = send_request(request_url, headers=headers, data=payload, method="POST")
    if not response or response.status_code != 200:
        return fb_source_data

    response = json.loads(response.text)
    result = response.get("result", {})
    title = result.get("title", "")  if result.get("title") else ""
    # 字符整理
    # 替换 \\n 为真正的换行符
    title = title.replace('\\n', '\n')

    # 正确解析 Unicode 转义字符
    title = bytes(title, "utf-8").decode("unicode_escape")

    # 可选：移除非法 surrogate（避免编码错误）
    title = re.sub(r'[\ud800-\udfff]', '', title)
    hd_video = result.get("sourceHd", "") if result.get("sourceHd") else ""
    sd_video = result.get("sourceSd", "") if result.get("sourceSd") else ""
    if hd_video and sd_video and title:
        fb_source_data = FacebookSource(
            title=title, hd_video_url=hd_video, sd_video_url=sd_video
        )

    return fb_source_data


def parse_getsave(url):
    request_url = "https://getsave.net/proxy.php"
    payload = {"url": url}
    headers = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "https://getsave.net",
        "priority": "u=1, i",
        "referer": "https://getsave.net/zh",
        "sec-ch-ua": '"Microsoft Edge";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": random_ua(),
        "x-requested-with": "XMLHttpRequest",
    }
    fb_source_data = None
    response = send_request(request_url, headers=headers, data=payload, method="POST")
    if not response or response.status_code != 200:
        return fb_source_data

    response = json.loads(response.text)
    result = response.get("api", {})
    if not result or result=='err':
        return fb_source_data
    title = result.get("title", "")
    if  title == "N/A":
        title ="No Title"
    
    # 多个清晰度视频，需要判断较高分辨率视频
    video_infos = result.get("mediaItems", [])
    hd_video_urls = [
        video_info
        for video_info in video_infos
        if video_info.get("mediaQuality", "") == "HD"
    ]
    if hd_video_urls:
        best_hd_info = max(hd_video_urls, key=lambda x: parse_resolution(x["mediaRes"]))
        hd_video = best_hd_info.get("mediaPreviewUrl", "")
    sd_video_urls = [
        video_info
        for video_info in video_infos
        if video_info.get("mediaQuality", "") == "SD" 
    ]
    if sd_video_urls:
        best_sd_info = max(sd_video_urls, key=lambda x: parse_resolution(x["mediaRes"]))
        sd_video = best_sd_info.get("mediaPreviewUrl", "")
    if hd_video and sd_video and title:
        fb_source_data = FacebookSource(
            title=title, hd_video_url=hd_video, sd_video_url=sd_video
        )

    return fb_source_data


def parse_resolution(res_str):
    match = re.match(r"(\d+)p", res_str)
    return int(match.group(1)) if match else 0
