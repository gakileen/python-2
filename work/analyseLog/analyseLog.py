#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
from time import mktime
from datetime import datetime
from pymongo import MongoClient

def analyseLog():

    local_file_name = '/Users/acmac/xxx/result.log'

    mongoConn = MongoClient("localhost",27017)
    db = mongoConn.dm
    analyse = db.analyse

    analyse.remove({})

    with open(local_file_name, 'r') as f:
        for line in f:
            parts = line.split(",")

            uid = parts[1].strip()
            t1 = int(parts[2].strip())
            t2 = int(parts[3].strip())

            analyse.insert({"uid":uid, "t1":t1, "t2":t2})

if __name__ == '__main__':
    analyseLog()