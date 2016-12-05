import os
import sys
import random

sys.path.append(os.path.abspath(os.path.dirname(__file__)) + '/../../acpy2')
reload(sys)
sys.setdefaultencoding('utf8')

from helpers.mongo_clusters import MONGO_KY_SHOCKINGS

coll_group = MONGO_KY_SHOCKINGS.smq.smq_group
coll_file = MONGO_KY_SHOCKINGS.smq.recommend


def batch_insert_group():
    tag_list = ['tag0', 'tag1', 'tag2', 'tag3', 'tag4', 'tag5', 'tag6', 'tag7', 'tag8', 'tag9']

    for i in range(0, 100):
        res = []
        for l in random.sample(range(0, 1000), 20):
            res.append(long(l))

        try:
            coll_group.insert_one({'_id': long(i),
                                   'n': 'group_name_' + str(i),
                                   'o': str(10000 + i),
                                   'a': 'group_announcement_' + str(i),
                                   'i': 'group_introduce_' + str(i),
                                   'jm': 1,
                                   'bim': 1,
                                   'im': 1,
                                   'utm': 1,
                                   'upm': 1,
                                   'tag': random.sample(tag_list, 2),
                                   'res': res,
                                   'ct': random.randint(0, 100000),
                                   'ut': random.randint(0, 100000)
                                   })
        except:
            print i


def batch_insert_file():
    for i in range(0, 1500):
        try:
            coll_file.insert_one({'_id': long(i),
                                  'uid': str(10000 + i),
                                  'fname': 'file_name_' + str(i),
                                  'md5': 'md5+' + str(i),
                                  'fsize': long(1024),
                                  'thumb': str(i),
                                  'time': long(1000000 + i),
                                  'path': '/storage/emulated/0/zapya/video/%d.mp4' % i,
                                  'category': 'video',
                                  'dura': long(0),
                                  'artist': '<unknown>',
                                  'cpt': 0,
                                  'ac': 0,
                                  'pos': (1 if i % 2 == 1 else 2) if i < 1000 else 0
                                  })
        except:
            print i


if __name__ == '__main__':
    batch_insert_group()
    batch_insert_file()
