import re
from datetime import datetime
from fastapi import HTTPException
from utils.log_utils import logger_access
from starlette.middleware.base import BaseHTTPMiddleware

# 定义可疑 User-Agent 的模式
SUSPICIOUS_PATTERNS = [
    re.compile(r"bot", re.IGNORECASE),
    re.compile(r"crawler", re.IGNORECASE),
    re.compile(r"spider", re.IGNORECASE),
    re.compile(r"python-requests", re.IGNORECASE),
    re.compile(r"curl", re.IGNORECASE),
    re.compile(r"scrapy", re.IGNORECASE),
    re.compile(r"wget", re.IGNORECASE),
    re.compile(r"httpclient", re.IGNORECASE),
    re.compile(r"java/", re.IGNORECASE),
    re.compile(r"phantomjs", re.IGNORECASE),
    re.compile(r"^mozilla/5\.0$", re.IGNORECASE),  # 精确匹配 Mozilla/5.0
]

# 定义 User-Agent 最小长度
MIN_USER_AGENT_LENGTH = 20  # 正常浏览器的 User-Agent 通常较长

class TokenVerifyMiddleware(BaseHTTPMiddleware):
    # dispatch 必须实现
    async def dispatch(self, request, call_next):
        client_host = request.client.host if request.client and request.client.host else "unknown"
        user_agent = request.headers.get("User-Agent", "").strip()
            # 检查是否缺少 User-Agent
        if not user_agent:
            logger_access.warning(f"Blocked request from {request.client.host}: No User-Agent provided")
            raise HTTPException(status_code=403, detail="No User-Agent provided")
        
        # 检查 User-Agent 长度
        if len(user_agent) < MIN_USER_AGENT_LENGTH:
            logger_access.warning(f"Blocked request from {request.client.host}: User-Agent too short: {user_agent}")
            raise HTTPException(status_code=403, detail="User-Agent too short")
        
        # 检查是否匹配可疑模式（包括 Mozilla/5.0）
        for pattern in SUSPICIOUS_PATTERNS:
            if pattern.search(user_agent.lower()):
                logger_access.warning(
                    f"Blocked request from {client_host} at {datetime.utcnow().isoformat()}: "
                    f"Suspicious User-Agent: {user_agent}, Method: {request.method}, Path: {request.url.path}"
                )
                raise HTTPException(status_code=403, detail="Suspicious User-Agent detected")
        
        # 继续处理正常请求
        response = await call_next(request)
        return response
