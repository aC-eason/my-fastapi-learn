from utils.common_utils import (
    is_facebook_video_post,
    is_pinterest_post,
    is_instrrgam_url,
)
from utils.facebook_downloader import parse_tools360, parse_getfb, parse_getsave
from utils.instargam_downloader import instargam_api, parse_snapdownload
from utils.pinterest_downloader import (
    parse_pinterestdownloader,
    parse_pokopin,
    parse_thepindown,
)


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

    def download_pinterest_source(self, pin_url: str):

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

    def download_instargam_source(self, ins_url: str):
        source_url = []
        source_type = 0
        ins_type, short_code = is_instrrgam_url(ins_url)
        source_type, source_url = instargam_api(short_code)
        if not source_url:
            source_url = parse_snapdownload(ins_url)
            if ins_type == "reel":
                source_type = 2
            else:
                if len(source_url) > 1:
                    source_type = 3
                elif len(source_url) == 1:
                    source_type = 1
                else:
                    source_type = 0
        return {"type": source_type, "source_url": source_url}


video_service = VideoService()
