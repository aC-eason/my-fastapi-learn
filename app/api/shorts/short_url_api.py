from utils.db_utils import get_db
from sqlalchemy.orm import Session
from common.cache import TOKEN_CACHE
from body.video_body import ShortUrlBody
from service.short_url_service import short_url_service
from fastapi.responses import JSONResponse,RedirectResponse
from fastapi import APIRouter, Request, status, Depends, Path


router = APIRouter(
    prefix="", tags=["用户登录"], responses={404: {"description": "Not found"}}
)


@router.post("/shorts")
def get_short_url_list(request: Request, db: Session = Depends(get_db)):
    is_login, user_id = check_login(request)
    resp = {"status": 200, "message": "", "shorts": []}
    if not is_login:
        resp["status"] = 401
        resp["message"] = "need login"
        return JSONResponse(content=resp)

    shorts = short_url_service.get_short_url_list(user_id)
    if not shorts:
        resp["status"] = 404
        resp["message"] = "no short urls found"
        return JSONResponse(content=resp)

    resp["shorts"] = shorts
    return JSONResponse(content=resp)


@router.post("/shorts/create")
def create_short_url(
    request: Request, website: ShortUrlBody, db: Session = Depends(get_db)
):
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

    short_code = short_url_service.create_short_url(
        origin_url=website.url, user_id=user_id, is_tracked=website.is_tracked
    )
    if not short_code:
        resp["status"] = 500
        resp["message"] = "create short url failed"
        return JSONResponse(content=resp)
    resp["message"] = "create short url success"
    resp["short_code"] = "https://kithubs.com/link/" + short_code
    return JSONResponse(content=resp)


@router.get(
    "/shorts/{short_code}",
)
def redirect_to_original_url(
    request: Request, short_code: str = Path(..., min_length=1)
):
    origin_url = short_url_service.get_url_info(short_code, request)
    if not origin_url:
        origin_url = "https://kithubs.com/short-url"
    return RedirectResponse(url=origin_url)


def check_login(request: Request):
    is_login = False
    user_id = None

    token = request.headers.get("Authorization", None)
    cache_info = TOKEN_CACHE.get(token)
    if cache_info:
        user_id = cache_info.get("user_id")
        is_login = True

    return is_login, user_id
