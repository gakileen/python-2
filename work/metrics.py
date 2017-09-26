#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import time
import logging
import pymongo
import redis
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from pymongo import MongoClient

reload(sys)
sys.setdefaultencoding('utf8')

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                filename='/home/deployer/chendx/logs/metrics_' + time.strftime('%Y_%m_%d')  + '.log',
                filemode='a')

#REDIS_HOST = "localhost"
#REDIS_PORT = 6379
REDIS_HOST = "ldkjserver0008"
REDIS_PORT = 6408
REDIS_DB = 0
redisConn = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

filePath = '/home/deployer/chendx/metrics/%s.csv'


def metrics():
	logging.info("------start...------")
	endPeriod = getEndPeriod()
	logging.info("endPeriod: %d" % (endPeriod))

	keys = redisConn.keys()
	for key in keys:
		try:
			parts = key.split(':')
			periodStr = parts[1]
			period = long(periodStr)

			if period < endPeriod:
				logging.info("---dealing: " + key)
				playid = parts[0]
				method = parts[2]

				fileName = filePath % (periodStr)
				fileExists = os.path.exists(fileName)
				file = open(fileName, 'a')

				if not fileExists:
					file.write('playId,handler,timestamp,duration,result,ip\n')

				records = redisConn.lrange(key, 0, -1)
				for record in records:
					recparts = record.split(',')
					start = recparts[0]
					duration = recparts[1]
					status = recparts[2]
					ip = recparts[3]

					file.write('%s,%s,%s,%s,%s,%s\n' % (playid, method, start, duration, status, ip))

				file.close()
				redisConn.delete(key)
		except:
			logging.error("dealing key [" + key + "] failed!")
	logging.info("------success------")

def getEndPeriod():
	return long(time.time() - 3600)

if __name__ == '__main__':
	metrics()
