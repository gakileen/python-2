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
                filename='/home/deployer/chendx/logs/wishes_' + time.strftime('%Y_%m_%d')  + '.log',
                filemode='a')

#mongoConn = MongoClient(['localhost:27017'])
mongoConn = MongoClient(['ldkjserver0014:27017'])
#mongoConn = MongoClient(['ldkjserver0003:54005','ldkjserver0004:54005','ldkjserver0005:54005','ldkjserver0006:54005'])
db = mongoConn.sfy
wishColl = db.wishes

def dropDups():
    logging.info("------start...------")

    keys = {}

    for wishDoc in wishColl.find().sort([('atf', pymongo.DESCENDING),('pos', pymongo.ASCENDING),('c@', pymongo.DESCENDING)]):
        on = wishDoc['on']
        if keys.has_key(on):
            logging.info('duplicate key %s' % on)
            wishColl.remove({'_id':wishDoc['_id']})
        else:
            keys[on]=1

    logging.info("------success------")

if __name__ == '__main__':
    dropDups()