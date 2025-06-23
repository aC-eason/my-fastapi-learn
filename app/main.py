from fastapi import FastAPI
from config.config import DEBUG
from starlette.middleware.cors import CORSMiddleware
from api.text_api.text_api import router as TextRouter
from api.common.common_api import router as CommonRouter
from api.video_api.video_api import router as VideoRouter
from api.user.user_api import router as UserRouter
from api.shorts.short_url_api import router as ShortUrlRouter
from midddlewares.UserLogMiddleware import UserLogMiddleWare

app = FastAPI()

app.include_router(CommonRouter, prefix="/api")
app.include_router(TextRouter, prefix="/api")
app.include_router(VideoRouter, prefix="/api")
app.include_router(UserRouter, prefix="/api")
app.include_router(ShortUrlRouter, prefix="/api")

app.add_middleware(UserLogMiddleWare)

if DEBUG:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
