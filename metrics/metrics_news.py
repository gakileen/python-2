#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import json
import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

sys.path.append(os.path.abspath(os.path.dirname(__file__)) + '/../../python-2')
from helpers.redis_clusters import NEWS_CN

REDIS_KEY_PREFIX = 'CLICK_DOCID_CN_'
FILE_PATH = '/usr/local/apps/DmTasks/shared/logs/news_metrics/'

REDIS_DB_METRICS = 4
REDIS_DB_CONTENT = 2
REDIS_CONN_METRICS = NEWS_CN._db(REDIS_DB_METRICS)
REDIS_CONN_CONTENT = NEWS_CN._db(REDIS_DB_CONTENT)


def generate_file():
    redis_key = REDIS_KEY_PREFIX + get_date_str()

    file_name = redis_key + '.txt'
    file_text = '------detail------\ndocid click_count channel title\n'

    news_count_total = REDIS_CONN_METRICS.zcard(redis_key)
    click_count_total = 0
    channel_news_count_dict = {}
    channel_click_count_dict = {}

    news_list = REDIS_CONN_METRICS.zrevrange(redis_key, 0, -1, True, int)
    for one_news in news_list:
        docid = one_news[0]
        click_count = one_news[1]
        click_count_total += click_count
        title = ''
        channel = ''

        content_str = REDIS_CONN_CONTENT.get(docid)
        if content_str:
            content_json = json.loads(content_str, encoding='utf-8')
            title = content_json['title'] if 'title' in content_json else ''
            channel = content_json['channel'] if 'channel' in content_json else ''

            channel_news_count_dict[channel] = 1 + (
                channel_news_count_dict[channel] if channel in channel_news_count_dict else 0)

            channel_click_count_dict[channel] = click_count + (
                channel_click_count_dict[channel] if channel in channel_click_count_dict else 0)

        file_text += '%s %d %s %s\n' % (docid, click_count, channel, title)

    channel_text = '------channel------\nchannel news_count click_count\n'
    channel_list = channel_news_count_dict.items()
    channel_list.sort(key=lambda x: x[1], reverse=True)
    for channel_tuple in channel_list:
        channel_code = channel_tuple[0]
        channel_text += '%s %d %d\n' % (channel_code, channel_tuple[1], channel_click_count_dict[channel_code])

    file_text = channel_text + '\n' + file_text

    file_text = '------general------\n[news_count_total]: %d  [click_count_total]: %d \n\n' % (
        news_count_total, click_count_total) + file_text

    file_object = open(FILE_PATH + file_name, 'w')
    file_object.write(file_text.encode('utf-8'))
    file_object.close()

    return file_name


def send_email(attach_name):
    # 设置登录及服务器信息
    mail_host = 'smtp.163.com'
    mail_user = 'ac_notice'
    mail_pass = 'password123'
    sender = 'ac_notice@163.com'
    receivers = ['dongxing.chen@dewmobile.net']

    # 设置eamil信息
    # 添加一个MIMEmultipart类，处理正文及附件
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = receivers[0]
    message['Subject'] = attach_name

    # 添加一个txt文本附件
    with open(FILE_PATH + attach_name, 'r')as h:
        content = h.read()
    # 设置txt参数
    part = MIMEText(content, 'plain', 'utf-8')
    # 附件设置内容类型，方便起见，设置为二进制流
    part['Content-Type'] = 'application/octet-stream'
    # 设置附件头，添加文件名
    part['Content-Disposition'] = 'attachment;filename=%s' % attach_name

    # 将内容附加到邮件主体中
    message.attach(part)

    # 登录并发送
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print('success')
        smtpObj.quit()
    except smtplib.SMTPException as e:
        print('error', e)


def get_date_str():
    now_time = datetime.datetime.now()
    yes_time = now_time + datetime.timedelta(days=-1)
    return yes_time.strftime('%Y%m%d')


if __name__ == '__main__':
    metrics_file_name = generate_file()
    send_email(metrics_file_name)
