from pymongo import MongoClient
from helpers.env import Env

MONGO_KY_RECS = MongoClient(Env().mongos_cluster("ky_recs"))
MONGO_KY_DM = MongoClient(Env().mongos_cluster("ky_dm"))
MONGO_KY_SHOCKINGS = MongoClient(Env().mongos_cluster("ky_shockings"))
