import json
from constent.text_api import TextAPI
from utils.request_utils import send_request


class TextService:

    def check_word(self, content):
        url = TextAPI.SENSITIVE_WORD_CHECK_URL.format(content)
        response = send_request(url=url)
        sensitive_word = ""
        has_sensitive_word = False
        if not response or response.status_code != 200:
            return has_sensitive_word, sensitive_word
        
        result = json.loads(response.text)
        num = result.get("num",0)
        if num == 1 or num =="1":
            has_sensitive_word = True
            sensitive_word = result.get("ci","")
        return has_sensitive_word, sensitive_word


text_service =TextService()

        



