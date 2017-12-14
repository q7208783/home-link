import redis

import config


class RedisPublisher(object):
    def __init__(self):
        self.pool = redis.ConnectionPool(host=config.RedisConfig.HOST_PORT, password=config.RedisConfig.PASSWORD,
                                         port=config.RedisConfig.PORT)
        self.strict_redis = redis.StrictRedis(connection_pool=self.pool)

    def publish(self, channel, msg):
        return self.strict_redis.publish(channel=channel, message=msg)
