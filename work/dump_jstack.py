#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import pymongo
from time import mktime
from datetime import datetime
from pymongo import MongoClient

reload(sys)
sys.setdefaultencoding('utf8')

mongoConn = MongoClient(['localhost:27017'])
db = mongoConn.test
jstackColl = db.jstack

def dump_jstack(file_path, file_name):
    read_file = file_path + file_name
    write_file = file_path + 'x/' + file_name

    infos = []
    with open(read_file, 'r') as r:
        for line in r:
            if "" != line and "\"" == line[0]:
                infos.append(line)
        infos.sort()

    with open(write_file, 'w') as w:
        for info in infos:
            w.write(info)

if __name__ == '__main__':
    file_path = '/Users/acmac/xxx/jstack/'
    file_name = '1.txt'

    if len(sys.argv) == 2:
        file_name = sys.argv[1]

    dump_jstack(file_path, file_name)