#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import yaml


class Env(object):
    """Running environment utils.

    Parses the env.yaml file and populates the environment related
    configuration values.

    """
    def __init__(self):
        self.conf = yaml.load(file(os.path.abspath(os.path.dirname(__file__)) + '/env.yaml', 'r'))

    def zookeeper_dbs(self):
        return self._parse('zookeeper', 'ensemble')

    def mongos_cluster(self, cluster):
        return self._parse("mongos", cluster)

    def _parse(self, key, subkey):
        try:
            return self.conf[key][subkey]
        except:
            return None
