import os
import sys
import logging

import datetime

sys.path.append(os.path.abspath(os.path.dirname(__file__)) + '/../../acpy2')
reload(sys)
sys.setdefaultencoding('utf8')

from helpers.util import Util
Util.config_logging_scheduled_rolling("leya/rela_file_and_group")
from helpers.mongo_clusters import MONGO_KY_SHOCKINGS

coll_group = MONGO_KY_SHOCKINGS.leya.group
coll_group_record = MONGO_KY_SHOCKINGS.leya.group_record
coll_group_record_bulk = coll_group_record.initialize_ordered_bulk_op()
coll_file_bulk = MONGO_KY_SHOCKINGS.leya.recommend.initialize_ordered_bulk_op()


def sort_file():
    logging.info("-------------start-----------")

    logging.info("get last time")
    last_time = datetime.datetime.utcfromtimestamp(0)

    last_time_doc = coll_group_record.find_one({'_id': 0})
    if last_time_doc:
        last_time = last_time_doc['last_time']

    logging.info("---------get all group")
    group_cursor = coll_group.find({'ut': {'$gt': last_time}},
                                   {'_id': 1, 'res': 1, 'jm': 1, 'o': 1, 'ut': 1}).sort('ut', 1)

    handle_group_count = 0
    for one_group in group_cursor:
        last_time = one_group['ut']

        jm = one_group['jm']
        o = None
        if 'o' in one_group:
            o = one_group['o']

        group_type = None
        if o:
            if jm == 0:
                group_type = 'gkq'
            else:
                group_type = 'smq'
        else:
            group_type = 'kkq'

        gid = one_group['_id']
        res = one_group['res']

        if res:
            newest_res = res[0: 5]
            group_record = coll_group_record.find_one({'_id': gid})
            if group_record:
                last_res_list = group_record['last_res']
                for last_res in last_res_list:
                    if last_res in res:
                        res = res[0: res.index(last_res)]
                        break

            if res:
                coll_file_bulk.find({'_id': {'$in': res}}).update({'$addToSet': {group_type: gid}})
                coll_group_record_bulk.find({'_id': gid}).upsert().update({'$set': {'last_res': newest_res}})
                handle_group_count += 1

    logging.info("---------execute bulk update")
    coll_group_record.update_one({'_id': 0}, {'$set': {'last_time': last_time}}, upsert=True)
    if handle_group_count > 0:
        coll_file_bulk.execute()
        coll_group_record_bulk.execute()
        logging.info("---------handled %d groups" % handle_group_count)

    logging.info("-------------end-----------")


if __name__ == '__main__':
    sort_file()
