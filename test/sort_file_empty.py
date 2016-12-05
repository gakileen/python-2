import os
import sys
import logging

sys.path.append(os.path.abspath(os.path.dirname(__file__)) + '/../../acpy2')
reload(sys)
sys.setdefaultencoding('utf8')

from helpers.util import Util
Util.config_logging_scheduled_rolling("sort_file")
from helpers.mongo_clusters import MONGO_KY_SHOCKINGS

coll_group = MONGO_KY_SHOCKINGS.leya.group
coll_file = MONGO_KY_SHOCKINGS.leya.recommend
coll_sorted_file = MONGO_KY_SHOCKINGS.leya.sorted_file


def sort_file():
    logging.info("-------------start-----------")

    all_file_list = []
    sort = 0

    # file_cursor = coll_file.find().sort('pc', -1).limit(1000)
    file_cursor = coll_file.find().sort('time', -1).limit(1000)

    for one_file in file_cursor:
        rid = one_file['_id']
        one_group = coll_group.find({'res': rid}).sort('ct', -1).limit(1)

        one_file['_id'] = '_' + str(rid)
        one_file['rid'] = rid
        one_file['sort'] = sort
        sort += 1

        for newest_group in one_group:
            gid = newest_group['_id']
            one_file['_id'] = str(gid) + '_' + str(rid)
            one_file['gid'] = gid
            one_file['gname'] = newest_group['n']

        all_file_list.append(one_file)
    logging.info("sort file in memory")

    if all_file_list:
        coll_sorted_file.delete_many({})
        logging.info("old data removed")

        coll_sorted_file.insert_many(all_file_list)
        logging.info("insert sorted file to mongodb")

    logging.info("-------------end-----------")


if __name__ == '__main__':
    sort_file()
