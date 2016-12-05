#!/usr/bin/env python
# -*- coding: utf-8 -*-

from redis_conns import RedisConns

NEWS_CN = RedisConns("news_cn")
NEWS_EN = RedisConns("news_en")
SHOCKINGS = RedisConns("shockings")
KY_HOME = RedisConns("ky_home")
