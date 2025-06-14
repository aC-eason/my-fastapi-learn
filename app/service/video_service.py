from utils.common_utils import is_facebook_video_post,is_pinterest_post
from utils.facebook_downloader import parse_tools360, parse_getfb, parse_getsave
from utils.pinterest_downloader import parse_pinterestdownloader,parse_pokopin,parse_thepindown


class VideoService:
    def download_facebook_video(self, fb_url):
        ret = {}
        if not is_facebook_video_post(url=fb_url):
            return ret
        parse_data = parse_getfb(url=fb_url)
        if not parse_data:
            parse_data = parse_tools360(fb_url)

        if not parse_data:
            parse_data = parse_getsave(url=fb_url)

        if not parse_data:
            return ret

        ret = {
            "sd_url": parse_data.sd_video_url if parse_data else "",
            "hd_url": parse_data.hd_video_url if parse_data else "",
            "title": parse_data.title if parse_data else "",
        }
        return ret
    
    def download_pinterest_source(self, pin_url:str):

        ret = {}
        if not is_pinterest_post(pin_url):
            return ret
        # 获取Pinterest的download url
        parse_data = parse_pokopin(pin_url)
        if not parse_data:
            parse_data = parse_pinterestdownloader(pin_url)
        if not parse_data:
            parse_data = parse_thepindown(pin_url)
        if parse_data:
            ret.update(parse_data)   
        
        return ret
        


video_service = VideoService()
