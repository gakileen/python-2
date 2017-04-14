#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re
import time
import requests
from bs4 import BeautifulSoup

sys.path.append(os.path.abspath(os.path.dirname(__file__)) + '/../../python/common')
from dbconns.mongo_db import MongoDB

mongo = MongoDB()
mongo.add_conn(cluster='stuff_prod', addr=["LDKJSERVER0003:54005","LDKJSERVER0004:54005","LDKJSERVER0005:54005","LDKJSERVER0006:54005"])
videos = mongo.coll('pearvideos', cluster='stuff_prod', db='videos')

def crawl_detail_page(url, tag):
    if videos.find_one({"bu":url}) != None:
        return

    n = ""
    desc = ""
    dt = long(0)
    u = ""
    tu = ""
    du = int(0)
    s = long(0)

    content = requests.get(url).content

    m = re.search("sdUrl=\"(.*)\",ldUrl", content)
    if m:
        u = m.groups(0)[0]

    if u == "" or (not u.endswith("mp4")):
        return

    s = long(requests.head(u).headers["Content-Length"])

    soup = BeautifulSoup(content, "html.parser")

    poster = soup.find("div", {"id" : "poster"})
    if poster != None:
        n = poster.find("img", {"class" : "img"})["alt"]
        tu = poster.find("img", {"class" : "img"})["src"]

    desc =  soup.find("meta", {"name" : "Description"})["content"]
    dt_str =  soup.find("div", {"class" : "date"}).text  # 2017-02-28 13:07
    dt = long(time.mktime(time.strptime(dt_str, "%Y-%m-%d %H:%M")) * 1000)

    payload = {}
    payload["n"] = n
    payload["desc"] = desc
    payload["dt"] = dt
    payload["u"] = u
    payload["tu"] = tu
    payload["du"] = du
    payload["s"] = s
    payload["bu"] = url
    payload["t"] = tag

    if videos.find_one({"bu":url}) == None:
        videos.insert(payload)

def crawl_category(url, tag):
    content = requests.get(url).content
    soup = BeautifulSoup(content, "html.parser")

    for a in soup.find_all("a", {"class" : "vervideo-lilink actplay"}):
        crawl_detail_page("http://www.pearvideo.com/" + a["href"], tag)

if __name__ == "__main__":
    crawl_category("http://www.pearvideo.com/category_1", u"社会")
    crawl_category("http://www.pearvideo.com/category_4", u"娱乐")
    crawl_category("http://www.pearvideo.com/category_7", u"搞笑")
    crawl_category("http://www.pearvideo.com/category_9", u"体育")
