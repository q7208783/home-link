import time

from utils.RedisPublisher import RedisPublisher

publisher = RedisPublisher()
i = 1
while (True):
    subnum = publisher.publish("hello", i)
    i = i + 1
    print 'subnum:' + str(subnum)
    print 'msg:' + str(i)
    time.sleep(1)
