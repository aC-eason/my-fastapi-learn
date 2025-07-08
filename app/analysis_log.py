import time
from common.cache import VISIT_SHORT_URL_CACHE
from utils.mongodb_utils import MongoDBClient


mongo_client = MongoDBClient()

def get_short_url_visit_info(current_time):
    visit_detail = {}

    while True:
        cisit_info = VISIT_SHORT_URL_CACHE.dequeue()
        if cisit_info is None:
            break

        short_code = cisit_info["short_code"]
        request_time = cisit_info["time"]
        if request_time >= current_time:
            break
        if not visit_detail.get(short_code):
            visit_detail[short_code] = 1
        else:
            visit_detail[short_code] += 1


def work():
    visit_info =[]
    while True:
        cisit_info = VISIT_SHORT_URL_CACHE.dequeue()
        if cisit_info is None:
            time.sleep(5 * 60)
            continue
        visit_info.append(cisit_info)
        if len(visit_info) >= 50:
            mongo_client.insert_many_visit_info(visit_info)
            visit_info = []

if __name__ == "__main__":
    work()
