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
                filename='/home/deployer/chendx/logs/uuid_' + time.strftime('%Y_%m_%d')  + '.log',
                filemode='a')

#mongoConn = MongoClient(['localhost:27017'])
#mongoConn = MongoClient(['ldkjserver0014:27017'])
mongoConn = MongoClient(['ldkjserver0003:54001','ldkjserver0004:54001','ldkjserver0005:54001','ldkjserver0006:54001'])
db = mongoConn.zl
plansColl = db.plans

aid = '5746c7653306f7dea3099556'

def dumpPlanUuid(fileName):
    logging.info("------start...------")

    with open(fileName, 'r') as f:
        for line in f:
            try :
                if line.isspace():
                    continue

                line = line.replace("\r\n", "")
                parts = line.split(' ')

                uuid = parts[1]
                plan = int(parts[2])

                plansColl.insert({'aid':aid, 'uuid':uuid, 'plan':plan})
            except:
                logging.error("dump line [" + line + "] failed!")

    logging.info("------success------")

if __name__ == '__main__':
    argvCount = len(sys.argv)

    if argvCount == 2:
        fileName = sys.argv[1]
        dumpPlanUuid(fileName)
    elif argvCount == 1:
        print "please give the filename"
    else:
        print "error count of argv"