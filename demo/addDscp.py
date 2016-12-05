#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import pymongo
import time
import logging
import traceback
import redis
import json
import hashlib
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from pymongo import MongoClient

reload(sys)
sys.setdefaultencoding('utf8')

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                filename='/home/deployer/chendx/logs/addDscp_' + time.strftime('%Y_%m_%d')  + '.log',
                filemode='a')

#mongoConn = MongoClient(['localhost:27017'])
mongoConn = MongoClient(['ldkjserver0005:54005'])
db = mongoConn.dm
shockingsColl = db.shockings
materialsColl = db.materials

def addDscp():
	logging.info("------create material dict start------")
	materialDict = {}
	materialList = materialsColl.find()
	for oneMaterial in materialList:
		key = oneMaterial['pkg']
		value = oneMaterial['description']
		materialDict[key] = value
	logging.info("------create material dict end------")


	logging.info("------update shockings start------")
	shockingList = shockingsColl.find({'type':5})
	#shockingList = shockingsColl.find({"uid" : "20109", "name" : "万能影视"})
	count = 0
	for oneShocking in shockingList:
		try :
			if 'dscp' in oneShocking:
				continue

			pkg = oneShocking['pkg']
			if materialDict.has_key(pkg):
				dscp = materialDict[pkg]
				_id = oneShocking['_id']
				shockingsColl.update_one({'_id':_id}, {'$set' : {'dscp' : dscp}})
		except:
			logging.info("update shockings [" + str(oneShocking) + "] failed.")

		count += 1
		if count%1000 == 0:
			logging.info("updated " + str(count))
	logging.info("------update shockings end------")


if __name__ == '__main__':
    addDscp()