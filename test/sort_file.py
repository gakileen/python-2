import os
import sys
import logging

sys.path.append(os.path.abspath(os.path.dirname(__file__)) + '/../../acpy2')
reload(sys)
sys.setdefaultencoding('utf8')

from helpers.util import Util
Util.config_logging_scheduled_rolling("leya/sort_file")
from helpers.mongo_clusters import MONGO_KY_SHOCKINGS

coll_file = MONGO_KY_SHOCKINGS.leya.recommend
coll_file_bulk = coll_file.initialize_ordered_bulk_op()


def sort_file():
    logging.info("-------------start-----------")

    file_sort_dict = {}
    sort_file_tuple_list = []

    logging.info("order by time")
    time_sort = 0
    time_file_cursor = coll_file.find({}, {'_id': 1}).sort('time', -1)
    for one_file in time_file_cursor:
        time_sort += 1
        file_sort_dict[one_file['_id']] = time_sort

    logging.info("order by download times")
    dlt_sort = 0
    dlt_file_cursor = coll_file.find({}, {'_id': 1}).sort([('dlt', -1), ('time', -1)])
    for one_file in dlt_file_cursor:
        dlt_sort += 1
        _id = one_file['_id']
        sort_file_tuple_list.append((file_sort_dict[_id] + dlt_sort, _id))

    logging.info("sort list")
    sort_file_tuple_list.sort()

    logging.info("update mongodb")
    for sort_file_tuple in sort_file_tuple_list:
        coll_file_bulk.find({'_id': sort_file_tuple[1]}).update_one({'$set': {'sort': sort_file_tuple[0]}})
    coll_file_bulk.execute()

    logging.info("-------------end-----------")


if __name__ == '__main__':
    sort_file()
