from utils.facebook_downloader import parse_tools360, parse_getfb, parse_getsave


class VideoService:
    def download_facebook_video(self, fb_url):
        ret = {}
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


video_service = VideoService()
