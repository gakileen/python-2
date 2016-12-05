#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import datetime
import logging
import os
import errno

logpath = '/usr/local/apps/DmTasks/shared/logs'


class Util(object):
    """Provide some utility functions which can be globally used."""

    @staticmethod
    def current_time_millis():
        """Returns current unix timestamp in milli seconds."""
        delta = datetime.datetime.utcnow() - datetime.datetime.utcfromtimestamp(0)
        return long(delta.total_seconds() * 1000)

    @staticmethod
    def start_of_today_millis():
        """Returns start of today timestamp in milli seconds."""
        today = datetime.datetime.utcnow()
        start_of_today = datetime.datetime(today.year, today.month, today.day)
        delta = start_of_today - datetime.datetime.utcfromtimestamp(0)
        return long(delta.total_seconds() * 1000)

    @staticmethod
    def mkdir_p(path):
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise

    @staticmethod
    def yesterday_str():
        yesterday =  datetime.datetime.now() - datetime.timedelta(days=1)
        return yesterday.strftime('%Y-%m-%d')


    @staticmethod
    def config_logging_scheduled(log_file_name):
        """Config the log file path for scheduled tasks."""
        logging.basicConfig(filename='%s/scheduled/%s.log' % (logpath, log_file_name),
                            format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO, filemode='a')

    @staticmethod
    def config_logging_scheduled_rolling(log_file_name):
        """Config the log file path for scheduled tasks."""
        logging.basicConfig(filename='%s/scheduled/%s_%s.log' % (logpath, log_file_name, time.strftime('%Y_%m_%d')),
                            format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO, filemode='a')

    @staticmethod
    def config_logging_daemon(log_file_name):
        """Config the log file path for scheduled tasks."""
        logging.basicConfig(filename='%s/daemon/%s.log' % (logpath, log_file_name),
                            format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO, filemode='a')

    @staticmethod
    def config_logging_daemon_rolling(log_file_name):
        """Config the log file path for scheduled tasks."""
        logging.basicConfig(filename='%s/daemon/%s_%s.log' % (logpath, log_file_name, time.strftime('%Y_%m_%d')),
                            format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO, filemode='a')