#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import time


class myThread(threading.Thread):

    def __init__(self, threadID, name, delay):
        threading.Thread.__init__(self)
        self.threadId = threadID
        self.name = name
        self.delay = delay

    def run(self):
        print "Starting " + self.name

        threadLock.acquire()

        print_time(self.name, self.delay, 5)

        threadLock.release()

        print "Exiting " + self.name


def print_time(thread_name, deplay, count):
    while count:
        time.sleep(deplay)
        print "%s: %s" % (thread_name, time.ctime(time.time()))
        count -= 1

threadLock = threading.Lock()


thread1 = myThread(1, "Thread-1", 1)
thread2 = myThread(2, "Thread-2", 2)

thread1.start()
thread2.start()


threads = [thread1, thread2]

for t in threads:
    t.join()


print "Exiting Main Thread"
