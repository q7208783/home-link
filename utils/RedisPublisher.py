import redis

import config
from common.LogMgr import LogMgr

logger_publisher = LogMgr('publisher.log')


class RedisPublisher(object):
    def __init__(self):
        self.pool = redis.ConnectionPool(host=config.RedisConfig.HOST_PORT, password=config.RedisConfig.PASSWORD,
                                         port=config.RedisConfig.PORT)
        self.strict_redis = redis.StrictRedis(connection_pool=self.pool)

    def publish(self, channel, msg):
        logger_publisher.info('channel:' + channel + 'msg:' + msg)
        return self.strict_redis.publish(channel=channel, message=msg)
