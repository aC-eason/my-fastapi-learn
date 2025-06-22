from crud.crud import user_dao
from fastapi import Request
from model.mysql.user import User
from sqlalchemy.orm import Session
from config.config import NO_LOGIN_AVATAR


class LoginService:
    def google_login(self, request: Request, google_user_info , db: Session,invite_code:str= None):
        gmail = google_user_info.get("email", None)
        google_avatar = google_user_info.get("picture", "")
        log_info = request.state.log_info

        user_info = {
            "user_id": None,
            "user_name": google_user_info.get("name", ""),
            "email": gmail,
            "avatar": NO_LOGIN_AVATAR,
            "ip": log_info.get("ip", ""),
            "login_time": log_info.get("request_time", 0),
        }

        user = user_dao.get_user(db=db, email=gmail)
        if user:
            # 更新用户登录ip 和登录时间,用户头像
            user_dao.update_user_login_info(
                db=db,
                email=gmail,
                last_login_ip=log_info.get("ip", ""),
                avatar=NO_LOGIN_AVATAR,
                google_avatar=google_avatar,
            )
        else:
            # 不存在用户
            new_user = User(
                email=gmail,
                user_name=google_user_info.get("name", ""),
                avatar=NO_LOGIN_AVATAR,
                raw_avatar=google_avatar,
                register_ip=log_info.get("ip", ""),
                user_type=1,  # google登录用户默认为 1
                status=1,
                last_login_ip=log_info.get("ip", ""),
            )
            if  invite_code:
                new_user.invite_code = invite_code
            user = user_dao.create_user(db=db, new_user=new_user)

        # token 解析出用户信息 存放到redis中
        # user_info["avatar"] =  NO_LOGIN_AVATAR
        user_info["user_id"] = user.id if user else ""
        user_info["email"] = user.email if user else ""
        log_info["user_id"] = user.id if user else None  # 阿里云日志记录为数据库用户id
        request.state.log_info = log_info
        return user_info
    


login_service = LoginService()
