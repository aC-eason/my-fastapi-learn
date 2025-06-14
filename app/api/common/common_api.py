import time
from urllib.parse import urlparse
from common.cache import VISIT_INFO
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Request, status, Path


router = APIRouter(tags=["通用api"], responses={404: {"description": "Not found"}})

@router.post("/collect")
def record_vist_info( request: Request):
    referer = request.headers.get("referer", "")
    today_str = time.strftime("%Y%m%d")
    cache_detail = VISIT_INFO.get(today_str)
    if not cache_detail:
        cache_detail={}
    try:
        if referer:
            parsed_url = urlparse(referer)
            url = parsed_url.path
            today_visit_count = cache_detail.get(url, 0)
            today_visit_count += 1
            cache_detail[url] = today_visit_count
    except BaseException as e:
        print("无效访问地址")
        
    VISIT_INFO.set(today_str, cache_detail)
    return  JSONResponse({"status":200})


