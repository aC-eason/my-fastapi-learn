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
from body.login_body import  GoogleLogin



router = APIRouter(
    prefix="/user", tags=["用户登录"], responses={404: {"description": "Not found"}}
)


@router.post("/google-login")
def google_login(
    request: Request, login_form: GoogleLogin, db: Session = Depends(get_db)
):
    google_user_info = verify_google_token(login_form.client_id)
    if not google_user_info:
        return JSONResponse(
            {"status": 401, "message": "token is invalid"},
            status_code=status.HTTP_200_OK,
        )

    user_info = login_service.google_login(
        request,
        db=db,
        google_user_info=google_user_info,
        invite_code=login_form.invite_code,
    )
    user_token = login_form.client_id
    # 缓存token 解析信息
    TOKEN_CACHE.set(user_token, user_info, 60 * 60 * 24 * 7)
    ret = {"token": user_token}
    return JSONResponse({"status":200,"data":ret}, status_code=status.HTTP_200_OK)


@router.get("/info")
def get_user_info(request: Request):
    token = request.headers.get("Authorization", None)
    user_info = TOKEN_CACHE.get(token)
    user_login_info = get_user_info_from_request(request)
    if not token or not user_login_info.is_login:
        return JSONResponse(
            {"status": 401, "message": "token is invalid or user not logged in"},
            status_code=status.HTTP_200_OK,
        )

    credit_info = credit_service.query_credit(user_info=user_login_info)
    if credit_info:
        user_info.update(credit_info)

    return JSONResponse({"status":200,"data":user_info}, status_code=status.HTTP_200_OK)