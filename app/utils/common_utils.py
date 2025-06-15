import re 
from urllib.parse import urlparse

def get_resolution(url):
    # 使用正则表达式提取分辨率
    match = re.search(r'(\d+)x', url)
    if match:
        return f"{match.group(1)}p"
    return ''

def is_facebook_video_post(url: str) -> bool:
    """
    检查是否是 Facebook 的视频帖子链接。

    :param url: 要检查的 URL。
    :return: 如果是 Facebook 视频帖子链接返回 True，否则返回 False。
    """
    is_fb_post = False
    fb_video_prefix =["www.facebook.com/","fb.watch"]
    for prefix in fb_video_prefix:
        if url.find(prefix) > -1:
            is_fb_post = True
            break
    
    return is_fb_post  


def is_pinterest_post(url: str) -> bool:
    """
    检查是否是 Pinterest 的帖子链接。

    :param url: 要检查的 URL。
    :return: 如果是 Pinterest 帖子链接返回 True，否则返回 False。
    """
    try:
        # 使用 urlparse 检查域名
        parsed_url = urlparse(url)
        if parsed_url.netloc.find('pin') > -1:
            return True
        return False
    except Exception as e:
        print(f"Error while checking URL: {e}")
        return False


def is_instrrgam_url(url:str):
    pattern = r"https?://(?:www\.)?instagram\.com/([a-zA-Z]+)/([A-Za-z0-9_-]+)(?:/|\?|$)"
    match = re.match(pattern, url)
    
    if match:
        primary_route = match.group(1)  # reel 或 p
        shortcode = match.group(2)      # DKtQ0xVSIgy 或 DKgOfvUhPsY
        # 验证一级路由是否为 reel 或 p
        if primary_route in ['reel', 'p']:
            return primary_route, shortcode
    return None, None