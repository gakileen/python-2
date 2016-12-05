#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import json
import logging
import redis
import zookeeper
from env import Env
sys.path.append(os.path.abspath(os.path.dirname(__file__)) + '/../../../python')


class RedisConns(object):
    zkHandler = zookeeper.init(Env().zookeeper_dbs())

    def __init__(self, cluster):
        self.cluster = cluster
        self.znode = '/redis_failover/' + cluster
        self.host = None
        self.port = None
        self.conns = {}

    def _db(self, db):
        if db not in self.conns:
            logging.info("[RedisConns %s] _db: init db[%d]" % (self.cluster, db))

            if self.host == None or self.port == None:
                self._conf_host_and_port_from_zk()

            self.conns[db] = redis.StrictRedis(host=self.host, port=self.port, db=db)

        return self.conns[db]

    def _zk_watch(self, handler, type, state, path):
        logging.info("[RedisConns %s] _zk_watch: type[%d], state[%d], path[%s]" % (self.cluster, type, state, path))

        if path == self.znode and type == 3:
            logging.info("[RedisConns %s] _zk_watch: zkvalue changed!" % self.cluster)

            changed = self._conf_host_and_port_from_zk()
            if changed:
                dbs = self.conns.keys()
                logging.info("[RedisConns %s] _zk_watch: host or port changed. Refresh all conns [%s] ..." % (self.cluster, str(dbs)))

                for db in dbs:
                    self.conns[db] = redis.StrictRedis(host=self.host, port=self.port, db=db)

                logging.info("[RedisConns %s] _zk_watch: Refresh conns OK!" % self.cluster)

    def _conf_host_and_port_from_zk(self):
        logging.info("[RedisConns %s] _conf_host_and_port_from_zk: begin..." % self.cluster)

        zk_value = zookeeper.get(RedisConns.zkHandler, self.znode, self._zk_watch)

        json_value = json.loads(zk_value[0])
        params = json_value['master'].split(':')
        new_host = params[0]
        new_port = int(params[1])

        changed = self.host != new_host or self.port != new_port
        if changed:
            self.host = new_host
            self.port = new_port

        logging.info("[RedisConns %s] _conf_host_and_port_from_zk: changed[%s]. host[%s], port[%d]" % (self.cluster, changed, new_host, new_port))

        return changed

    """
        implements StrictRedis's methods
    """

    def get(self, db, key):
        return self._db(db).get(key)

    def set(self, db, name, value, ex=None, px=None, nx=False, xx=False):
        return self._db(db).set(name, value, ex, px, nx, xx)

    def hset(self, db, name, key, value):
        return self._db(db).hset(name, key, value)

    def delete(self, db, *names):
        return self._db(db, *names)
