#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import time
import logging
import pymongo
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from pymongo import MongoClient

reload(sys)
sys.setdefaultencoding('utf8')

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                filename='/usr/local/apps/DmTasks/shared/logs/user_video_actions_' + time.strftime('%Y_%m_%d')  + '.log',
                filemode='a')

mongoConn = MongoClient(['localhost:27017'])
#mongoConn = MongoClient(['ldkjserver0014:27017'])
#mongoConn = MongoClient(['ldkjserver0003:54005','ldkjserver0004:54005','ldkjserver0005:54005','ldkjserver0006:54005'])

db = mongoConn.dm
actionColl = db.user.videoactions

def addCounter():
    logging.info("------start...------")

    c_record = 0

    for actDoc in actionColl.find({'flag': {'$exists': 0}}).limit(10):
        actions = actDoc.get('actions')
        if actions != None :
            counter_1 = len(filter(extract_consume, actions))
            counter_2 = len(filter(extract_dislike, actions))

            actionColl.update_one({'_id':actDoc['_id']}, {'$set':{'counter_1': counter_1, 'counter_2': counter_2, 'flag': 1}})

        c_record += 1

        if c_record % 1000 == 0:
            logging.info(c_record)
            
    logging.info("------success------")

def extract_consume(t):
    return t['aid'] == 1

def extract_dislike(t):
    return t['aid'] == 2


if __name__ == '__main__':
    addCounter()