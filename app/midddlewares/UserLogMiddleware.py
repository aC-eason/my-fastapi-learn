import time, json, io
from fastapi import Request
from starlette.responses import Response, StreamingResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from utils.log_utils import logger_access

from utils.common_utils import get_client_ip

# 1. 在FastAPI 中，当接口发生 500 错误时，错误处理流程通常是直接返回错误响应，而不会再经过中间件。
#    中间件是在请求处理过程中执行的，如果在处理请求时发生了未捕获的异常，FastAPI 会根据其异常处理机制直接生成错误响应。
# 2. 由于这些错误通常是在 FastAPI 应用外部的组件（如网关或负载均衡器）中引发的，它们不会经过 FastAPI 中的中间件或异常处理器。
#    相反，这些错误是由反向代理或其他服务返回给客户端的。

# 所以，500以下的响应由中间件捕获；500的响应由异常处理器捕获；500以上的请求，不做请求记录


async def read_resp_data(response: StreamingResponse):
    if isinstance(response, StreamingResponse):
        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk
        response_body = response_body.decode("utf-8")
        response_is_json = True

        try:
            response_data = json.loads(response_body)
        except Exception:
            response_data = response_body
            response_is_json = False

        modified_body = json.dumps(response_data).encode("utf-8")
        response = StreamingResponse(
            io.BytesIO(modified_body),
            status_code=response.status_code,
            headers=dict(response.headers),
        )
        response.headers["Content-Length"] = str(len(modified_body))

        if response_is_json:
            return response_data, response
        else:
            return None, response
    else:
        return None, response


class UserLogMiddleWare(BaseHTTPMiddleware):

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        hostname = request.url.hostname  # 请求域名
        user_agent = request.headers.get("user-agent", "-")  # UA标识
        start_time = int(round(time.time() * 1000))  # 开始时间毫秒
        request.state.req_start_time = start_time
        req_ip = get_client_ip(request)  # 用户IP
        log_info = {
            "user_agent": user_agent,
            "referer": hostname,
            "ip": req_ip,
            "user_id": 0,
            "method": request.method,
            "url": request.url.path,
            "request_time": start_time,
            "deal_time": 0,
            "status": "",
            "message": "",
        }
        request.state.log_info = log_info
        response = await call_next(request)
        end_time = int(round(time.time() * 1000))  # 结束时间毫秒
        log_info["deal_time"] = end_time - start_time  # 处理时间 毫秒
        log_info["status"] = response.status_code  # 响应状态
        # log_info["user_type"] = get_user_type(
        #     request
        # )  # 用户类型  website： 网站来源， Extension ： 插件来源

        response_data, response = await read_resp_data(response)
        if response_data and isinstance(response_data, dict):
            log_info["message"] = response_data.get("id", "")
        logger_access.info(log_info)
        return response
