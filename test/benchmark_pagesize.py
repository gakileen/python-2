import requests
import json
import sys
import time


for i in range(1000):
    time.sleep(0.2)
    resp = requests.get(url='http://127.0.0.1:9110/ngnj/item_rec/videos?uid=9990444&p=%d&channelId=3' % i)
    respContent = resp.content
    data = json.loads(respContent)['data']
    if len(data) < 8:
        print "page: %d  AAA: %d" % (i,len(data))

    count = 0
    for j in range(len(data) - 1):
        if data[j]['uid'] == data[j + 1]['uid']:
            count += 1
    if count > 0:
        print "page: %d  BBB: %d" % (i, count)
