import requests
import urllib
import re
import random
from time import sleep


def main():
    url = 'https://www.zhihu.com/question/22591304/followers'

    i = 1
    for x in xrange(20, 3600, 20):
        data = {'start': '0', 'offset': str(x), '_xsrf': 'a128464ef225a69348cef94c38f4e428'}
        content = requests.post(url, data=data, timeout=10).text
        print content


if __name__ == '__main__':
    main()
