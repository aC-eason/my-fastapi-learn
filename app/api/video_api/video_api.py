from fastapi import APIRouter, Request
from body.video_body import WebsiteInfo
from service.video_service import video_service
from fastapi.responses import JSONResponse

router = APIRouter(tags=["通用api"],prefix="/video", responses={404: {"description": "Not found"}})

@router.post("/facebook/download")
def download_faceboo_video(request:Request,web_info:WebsiteInfo):
    fb_info = video_service.download_facebook_video(web_info.url)
    resp = {
        "status":200 if fb_info else 404,
        "data":fb_info
    }
    return JSONResponse(resp)

@router.post("/pinterest/download")
def download_pinterest_source(request:Request,web_info:WebsiteInfo):
    pin_info = video_service.download_pinterest_source(web_info.url)
    resp = {
        "status":200 if pin_info else 404,
        "data":pin_info
    }
    return JSONResponse(resp)


@router.post("/instagram/download")
def download_pinterest_source(request:Request,web_info:WebsiteInfo):
    ins_info = video_service.download_instargam_source(web_info.url)
    resp = {
        "status":200 if ins_info.get("type") != 0 else 404,
        "data":ins_info
    }
    return JSONResponse(resp)



