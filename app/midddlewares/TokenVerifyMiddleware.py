
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


class TokenVerifyMiddleware(BaseHTTPMiddleware):
    # dispatch 必须实现
    async def dispatch(self, request, call_next):
        if request.method == "OPTIONS":
            return await call_next(request)

        # 判断request的路由是以/desktop开头
        user_id = request.headers.get("User-Id", None)
        if not user_id:
            return JSONResponse({}, status_code=401)
        request.state.user_id = user_id
        print("user_id", user_id)
        return await call_next(request)
