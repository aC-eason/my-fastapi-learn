from pydantic import BaseModel

class WebsiteInfo(BaseModel):
    url:str


class ShortUrlBody(WebsiteInfo):
    is_tracked: bool = False