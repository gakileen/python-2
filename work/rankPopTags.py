#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import pymongo
import time
import logging
from pymongo import ReadPreference

TAG_MONGO_HOST = "127.0.0.1"
TAG_MONGO_PORT = 27017
DATA_MONGO_HOST = "127.0.0.1"
DATA_MONGO_PORT = 27017

#TAG_MONGO_HOST = "LDKJSERVER0005"
#TAG_MONGO_PORT = 54001
#DATA_MONGO_HOST = "LDKJSERVER0005"
#DATA_MONGO_PORT = 54002

POP_TAGS_NUM = 50

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                filename='/Users/acmac/xxx/logs/rankPopTags_' + time.strftime('%Y_%m_%d')  + '.log',
                filemode='a')

tag_conn = pymongo.MongoClient(TAG_MONGO_HOST,TAG_MONGO_PORT)
tag_db = tag_conn.dm
popTagColl = tag_db.persona.popTag1
tagColl = tag_db.persona.tag

data_conn = pymongo.MongoClient(DATA_MONGO_HOST+':'+str(DATA_MONGO_PORT),readPreference='secondaryPreferred')
data_db = data_conn.dm
finiColl = data_db.get_collection('coll.finished', read_preference=ReadPreference.PRIMARY)
musicColl = data_db.persona.music
videoColl = data_db.persona.video
bookColl = data_db.persona.book

POP_TAGS = []

popCollName = "persona.popTag"
tagCollName = "persona.tag"

sleepTime = 600

def rankPopTags():
    logging.info("------BEGIN------")
    
    # get all tags
    logging.info("------get all tags start..------")
    tagList = tagColl.find({},{"tag":1,"#n":1,"_id":0},no_cursor_timeout=True)
    logging.info("------get all tags success------")


    # add all tags into list
    logging.info("------add all tags into list loop start..------")
    for oneTag in tagList:
        tag = oneTag["tag"]

        newsCount = 0
        if "#n" in oneTag:
            newsCount = oneTag["#n"]

        if newsCount > 0:
            musicCount = musicColl.count({"t.n":tag})
            videoCount = videoColl.count({"t.n":tag})
            bookCount = bookColl.count({"t.n":tag})

            totalUserCount = musicCount + videoCount + bookCount

            POP_TAGS.append((newsCount * totalUserCount, newsCount, totalUserCount, tag))
    logging.info("------add all tags into list loop success------")

    # sort list
    logging.info("------sort pop tags' list start..------")
    list.sort(POP_TAGS)
    logging.info("------sort pop tags' list success------")
    

    # remove popTag collection in mongo
    logging.info("------remove popTag collection start..------")
    popTagColl.delete_many({})
    logging.info("------remove popTag collection success------")

    # save pop tags to mongo
    savePopTags(POP_TAGS)

    logging.info("------END------")


def savePopTags(tagTupleList):
    logging.info("------save pop tags start..------")
    
    leng = POP_TAGS_NUM if len(tagTupleList) > POP_TAGS_NUM else len(tagTupleList)
    for index in range(leng):
        popTuple = list.pop(tagTupleList)
        tag = popTuple[3]
        userCount = popTuple[2]
        newsCount = popTuple[1]
        score = popTuple[0]

        # save to mongo
        popTagColl.insert_one({"tag":tag, "score":score, "userCount":userCount, "newsCount":newsCount, "u@":long(time.time())})

    logging.info("------save pop tags success------")
    

def nowTime():
    return long(time.time() * 1000)

def middleNigthTime():
    return long((time.time() - (time.time() % 86400) + time.timezone) * 1000)


if __name__ == '__main__':
    rankPopTags()
