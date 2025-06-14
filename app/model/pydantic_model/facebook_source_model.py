from pydantic import BaseModel
from typing import Union

class FacebookSource(BaseModel):
    hd_video_url: Union[str, None] = None
    sd_video_url: Union[str, None] = None
    title: str = ""
