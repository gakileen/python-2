# -*- coding: UTF-8 -*-

import requests
from bs4 import BeautifulSoup

content = requests.get('http://www.irna.ir/fa/rssfeed.aspx').content
soup = BeautifulSoup(content, 'html.parser')

channel_list = soup.find_all('tr', {'class': ['ItemAlt', 'Item']})

file_db_channel = open('db_channel.txt', 'w')
file_db_channel_irna = open('db_channel_irna.txt', 'w')

high_priority_channels = ["-1", "32", "89", "51", "52", "85", "14", "15", "370", "371", "133", "45", "13", "360", "216", "41", "47", "6", "18", "19", "195", "34", "43", "142", "194", "181", "211", "20", "9", "4", "145", "2", "3", "5"]

for one_channel in channel_list:
    tds = one_channel.find_all('td')
    origin_channel_id = tds[1].find('a')['href'][36:]
    uni_channel_code = tds[0].text.strip()

    priority = "h" if origin_channel_id in high_priority_channels else "m"

    file_db_channel.write(
        ('db.en.channel.insert({ "_id" : "%s", "desc" : "%s", "only_area" : [ "IR" ], "priority" : "%s" })\n'
        % (uni_channel_code, origin_channel_id, priority)).encode('UTF-8'))

    file_db_channel_irna.write(
        ('db.en.channel.irna.insert({ "_id" : "%s", "channel_code" : "%s" })\n'
        % (origin_channel_id, uni_channel_code)).encode('UTF-8'))

file_db_channel.close()
file_db_channel_irna.close()
