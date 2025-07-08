import time, logging, json
import urllib.parse
from fastapi import Request
from starlette import status
from pydantic import BaseModel
from logging.handlers import RotatingFileHandler
from utils.common_utils import get_user_type


def get_error_log_info(
    request: Request, tips: str = "", status_code: status = 500, message: str = ""
):
    # 获取日志中间的前置信息
    request.state.log_info["status"] = status_code
    request.state.log_info["deal_time"] = (
        int(round(time.time() * 1000)) - request.state.req_start_time
    )  # 处理时间 毫秒
    request.state.log_info["tips"] = tips
    request.state.log_info["message"] = message
    request.state.log_info["user_type"] = get_user_type(request)
    return request.state.log_info


def format_log_detail(detail, type: str, user_id=""):
    if isinstance(detail, dict):
        detail = json.dumps(detail)
    detail = {
        "user_id": user_id,
        "time": time.time(),
        "type": type,
        "detail": detail,
    }
    return detail


def save_model_name_state(request: Request, model: str):
    """保存模型类型到state中"""
    if  model and request:    
        request.state.log_info["model"] = model 






def save_params_state(request: Request, model: BaseModel):
    """保存请求参数到state中

    Args:
        request (Request): request
        model (BaseModel): pydantic model
    """
    # 只分析条件字段，暂不分析prompt 字段
    user_params = model.dict()
    if user_params.get("description"):
        request.state.log_info["prompt"] =  user_params["description"][:300]
        del user_params["description"]

    elif user_params.get("params"):
        del user_params["params"]
    request.state.log_info["user_params"] = urllib.parse.urlencode(user_params)


def __get_log(log_type: str):
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s -【%(module)s.%(funcName)s:%(lineno)s】 -【%(levelname)s 】 - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logger = logging.getLogger(log_type)
    logger.setLevel(logging.INFO)
    # 测试环境记录文件日志
    file_name = f"kithubs-{log_type}.log"
    file_handler = RotatingFileHandler(
        file_name, maxBytes=1024 * 1024 * 10, backupCount=3
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


# web 服务log
logger_access = __get_log("web")


