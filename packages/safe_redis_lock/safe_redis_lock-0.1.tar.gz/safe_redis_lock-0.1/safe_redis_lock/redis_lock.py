'''

使用set key value [EX seconds] [PX milliseconds] [NX|XX]来加锁

和lua脚本的方式来释放锁
'''

import redis
import time
import os


class RedisLock:
    def __init__(self, lock_timeout, pool: redis.ConnectionPool, force_run=False, block=True, sleep_time=0.05):
        '''

        :param lock_timeout: 锁的超时时间
        :param pool: 一个redis连接池
        :param force_run: 是否强制运行当获取不到锁的时候
        :param block: 获取不到锁的时候是否阻塞
        :param sleep_time: 当获取不到锁的时候去重试获取锁的事件间隔
        '''
        self.pool = pool
        self.key = '__Redis_Lock__24767ffe-9e60-44c0-bfbe-2a96d3f457cf'
        self.timeout = lock_timeout
        self.force_run = force_run
        self.release_lua = """
        local token = redis.call('get', KEYS[1])
        if not token or token ~= ARGV[1] then
            return 0
        end
        redis.call('del', KEYS[1])
        return 1
    """
        conn = redis.Redis(self.pool)
        self.release_script = conn.register_script(self.release_lua)
        self.block = block
        self.sleep_time = sleep_time

    def lock(self, func):
        def inner(*args, **kwargs):
            val = '{}-{}'.format(threading.current_thread().ident, os.getpid())
            acquired = False
            try:
                acquired = self.acquire(val)
                if acquired or self.force_run:
                    res = func(*args, **kwargs)
                    return res
                else:
                    raise AcquireFailException

            except Exception as e:
                raise e
            finally:
                if acquired:
                    self.release(val)

        return inner

    def acquire(self, value):
        try:
            conn = redis.Redis(connection_pool=self.pool)
            res = conn.set(self.key, value, ex=self.timeout, nx=1)
            if self.block:
                while not res:
                    time.sleep(self.sleep_time)
                    conn = redis.Redis(connection_pool=self.pool)
                    res = conn.set(self.key, value, ex=self.timeout, nx=1)
            return res
        except Exception as e:
            print(e)
            return False

    def release(self, value):
        return self.release_script(
            keys=[self.key],
            args=[value],
            client=redis.Redis(connection_pool=self.pool)
        )


class AcquireFailException(Exception):
    '''
    raise the Exception when can not get lock

    '''


if __name__ == '__main__':
    import threading

    pool = redis.ConnectionPool(host='127.0.0.1', port=6379, password='lyc', db=0)

    conn = redis.Redis(connection_pool=pool)

    conn.set('producer', 10000)
    redis_lock_ = RedisLock(lock_timeout=5, pool=pool, block=True)


    @redis_lock_.lock
    def consumer_pp(conn):
        num = int(conn.get('producer'))
        if num == 0:
            return True
        else:
            print(f'we consumer one left --> {num}')
            conn.set('producer', num - 1)


    def consumer():
        pool = redis.ConnectionPool(host='127.0.0.1', port=6379, password='lyc', db=0)
        while True:
            conn = redis.Redis(connection_pool=pool)
            if consumer_pp(conn):
                break


    def consumer_thread():
        from threading import Thread
        for i in range(1):
            Thread(target=consumer).start()


    consumer_thread()
