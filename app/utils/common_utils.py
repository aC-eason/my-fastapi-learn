import re 
from fastapi import Request
from urllib.parse import urlparse
from google.oauth2 import id_token
from config.config import GOOGLE_CLIENT_ID
from google.auth.transport.requests import Request
from model.pydantic_model.user_info import UserInfo
import random
import string

def generate_short_code(length=6):
    """生成6位随机短链code，仅包含大小写字母和数字"""
    characters = string.ascii_letters + string.digits  # a-z, A-Z, 0-9
    return ''.join(random.choice(characters) for _ in range(length))





def verify_google_token(id_token_str):
    try:
        # 使用 Google 的公钥验证 token
        id_info = id_token.verify_oauth2_token(id_token_str, Request(), GOOGLE_CLIENT_ID)
        return id_info
    except ValueError as e:
        # 处理无效 token 错误
        return None
    
    



def get_client_ip(request: Request):
    """获取客户端IP"""
    # 获取用户真实IP
    user_ip = request.headers.get("cf-connecting-ip")
    if not user_ip:
        user_ip = request.headers.get("x-original-forwarded-for")
        if not user_ip:
            user_ip = request.client.host
    return user_ip

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


def get_user_info_from_request(request: Request):
    user_id = request.state.log_info.get("user_id", 0)
    is_login = False

    if user_id and user_id > 0:
        is_login = True
    else:
        user_id = request.headers.get("User-Id", 0)

    return UserInfo(user_id=user_id, is_login=is_login)