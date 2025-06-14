from fastapi import APIRouter, Request
from body.video_body import WebsiteInfo
from service.video_service import video_service
from fastapi.responses import JSONResponse

router = APIRouter(tags=["通用api"],prefix="/video", responses={404: {"description": "Not found"}})

@router.post("/facebook/download")
def senesitive_word_check(request:Request,web_info:WebsiteInfo):
    fb_info = video_service.download_facebook_video(web_info.url)
    resp = {
        "status":200 if fb_info else 404,
        "data":fb_info
    }
    return JSONResponse(resp)
