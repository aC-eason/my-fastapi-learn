import time
from common.cache import VISIT_SHORT_URL_CACHE
from wrapper.db_wrapper import with_mongo_db_client


@with_mongo_db_client
def work(mongo_client=None):
    visit_info =[]
    while True:
        print("进入循环")
        cisit_info = VISIT_SHORT_URL_CACHE.dequeue()
        if cisit_info is None:
            print("队列暂无数据")
            mongo_client.insert_many_visit_info(visit_info)
            time.sleep(5 * 60)
            continue
        print("取出数据:",cisit_info)
        visit_info.append(cisit_info)
        if len(visit_info) >= 50:
            mongo_client.insert_many_visit_info(visit_info)
            visit_info = []

if __name__ == "__main__":
    work()
