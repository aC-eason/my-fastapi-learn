
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