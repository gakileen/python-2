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
#mongoConn = MongoClient(['ldkjserver0014:27017'])
mongoConn = MongoClient(['ldkjserver0003:54005','ldkjserver0004:54005','ldkjserver0005:54005','ldkjserver0006:54005'])
db1 = mongoConn.sfy
newColl = db1.wishes

db2 = mongoConn.dm
wishesColl = db2.wishes.wishes
stuffColl = db2.wishes.stuff

def dumpWishes(fileName):
    logging.info("------start...------")

    with open(fileName, 'r') as f:
        for line in f:
            try :
                if line.isspace():
                    continue

                wid = line.replace("\n", "")

                onewish = wishesColl.find_one({'_id':wid})

                if onewish == None:
                    continue

                c_stuff = stuffColl.count({'wid': wid})
                wishesColl.update_one({'_id':wid}, {'$set':{'flag':c_stuff}})

                if c_stuff == 0:
                    continue

                onestuff = stuffColl.find_one({'wid': wid})

                name = onewish['keyword'][0]
                tag = onewish['tag']
                time = onewish['time']
                url = onestuff['url']
                thumb = onestuff['thumb']
                cat = onestuff['cat']
                size = onestuff['size']
                du = onestuff['du']
                uid = onestuff['uid']
                expire = 1496246400000

                newColl.insert({'_id':wid, 'on':name, 'tag':tag, 'bonus':0, 'type':0, 'atf':False, 'c@':time, 'u@':time, 'state':1, 'total':0, 'count':0, 'url':url, 'e@':expire, 'thumb':thumb, 'cat':cat, 'size':size, 'du':du, 'taken':0, 'like':0, 'dislike':0, 'uid':uid})

            except:
                logging.error("dump line [" + line + "] failed!")

    logging.info("------success------")

if __name__ == '__main__':
    argvCount = len(sys.argv)

    if argvCount == 2:
        fileName = sys.argv[1]
        dumpWishes(fileName)
    elif argvCount == 1:
        print "please give the filename"
    else:
        print "error count of argv"