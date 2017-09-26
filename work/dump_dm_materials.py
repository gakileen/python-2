#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
from time import mktime
from datetime import datetime
import pyhs2 as hive
sys.path.append(os.path.abspath(os.path.dirname(__file__)) + '/../../python/common')
from dbconns.mongo_db import MongoDB

def dump_dm_materials(mongo, daystr):
    mongo.add_conn(cluster='dm', addr=["LDKJSERVER0003:54005","LDKJSERVER0004:54005","LDKJSERVER0005:54005","LDKJSERVER0006:54005"])
    materials = mongo.coll('materials', cluster='dm', db='dm')
    file_name = 'dm_materials.%s.txt' % (daystr)

    local_file_name = './%s' % (file_name)
    os.system('hive -S -e "select id,name,description,detail,url,thumb,filename,filesize,md5,pkg,pkv,category,weight,priority,netgame,flag,create_time,update_time,removed,support_area,exclude_area from dictionary.materials where priority=0" > %s' % (file_name))
    materials.remove({})
    with open(local_file_name, 'r') as f:
        for line in f:
            line = line.replace("\n", "")
            parts = line.split("\t")

            removed = parts[18]

            if "true"==removed:
                continue

            _id = parts[0]
            name = parts[1]
            description = parts[2]
            detail = parts[3]
            url = parts[4]
            thumb = parts[5]
            filename = parts[6]
            filesize = parts[7]
            md5 = parts[8]
            pkg = parts[9]
            pkv = parts[10]
            category = parts[11]
            weight = parts[12]
            priority = parts[13]
            netgame = parts[14]
            flag = parts[15]
            create_time = long(mktime(time.strptime(parts[16], "%Y-%m-%d %H:%M:%S.%f"))) * 1000
            update_time = long(mktime(time.strptime(parts[17], "%Y-%m-%d %H:%M:%S.%f"))) * 1000
            support_area = parts[19]
            exclude_area = parts[20]

            materials.insert({"_id":_id, "name":name, "description":description, "detail":detail, "url":url, "thumb":thumb, "filename":filename, "filesize":filesize, "md5":md5, "pkg":pkg, "pkv":pkv, "category":category, "weight":weight, "priority":priority, "netgame":netgame, "flag":flag, "support_area":support_area, "exclude_area":exclude_area, "c@":create_time, "u@":update_time})

if __name__ == '__main__':
    mongo = MongoDB()
    daystr = time.strftime("%Y-%m-%d")
    dump_dm_materials(mongo, daystr)
