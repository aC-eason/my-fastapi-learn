
import json
from utils.db_utils import get_db
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from utils.common_utils import verify_google_token
from service.user_service import login_service
from common.cache import TOKEN_CACHE
from fastapi import APIRouter, Request, status, Depends, Path
from utils.common_utils import get_user_info_from_request
# from fastapi.responses import RedirectResponse
from body.video_body import ShortUrlBody
from service.short_url_service import short_url_service
from common.cache import TOKEN_CACHE
from fastapi.responses import RedirectResponse

router = APIRouter(
    prefix="/shorts", tags=["用户登录"], responses={404: {"description": "Not found"}}
)


@router.post("/create")
def create_short_url(request: Request, website: ShortUrlBody, db: Session = Depends(get_db)):
    is_login, user_id = check_login(request)
    resp = {
        "status": 200,
        "message": "",
    }
    if not is_login:
        resp["status"] = 401
        resp["message"] = "need login"
        return JSONResponse(content=resp)
    if not website.url:
        resp["status"] = 400
        resp["message"] = "url is required"
        return JSONResponse(content=resp)
    
    short_code = short_url_service.create_short_url(origin_url=website.url, user_id=user_id, is_tracked=website.is_tracked)
    if not short_code:
        resp["status"] = 500
        resp["message"] = "create short url failed"
        return JSONResponse(content=resp)
    resp["message"] = "create short url success"
    resp["short_code"] = "https://kithubs.com/link/"+short_code
    return JSONResponse(content=resp)


@router.get("/{short_code}")
def redirect_to_original_url(short_code: str = Path(..., min_length=1)):
    origin_url = "https://kithubs.com/short-url"
    cache_info  = short_url_service.get_url_info(short_code)
    if cache_info:
        origin_url = cache_info.get("original_url", origin_url)
    return RedirectResponse(url=origin_url)

    
    


def  check_login(request:Request):
    is_login = False
    user_id = None

    token = request.headers.get("Authorization", None)
    cache_info = TOKEN_CACHE.get(token)
    if cache_info:
        user_id = cache_info.get("user_id")
        is_login = True
    
    return is_login, user_id
    