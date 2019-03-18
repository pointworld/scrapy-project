import json
import redis
import pymongo

def main():
    # 指定 Redis 数据库信息
    redis_cli = redis.StrictRedis(host='192.168.1.114', port=6379, db=0)
    # 指定 MongoDB 数据库信息
    mongo_cli = pymongo.MongoClient(host='172.16.195.195', port=27017)


    # 创建数据库名
    db = mongo_cli['youyuan']
    # 创建表名
    sheet = db['guangdong_2019_03_11']

    while True:
        # FIFO 模式为 blpop， LIFO 模式为 brpop，获取键值
        source, data = redis_cli.blpop(['yy:items'])

        item = json.loads(data)
        sheet.insert(item)

        try:
            print('Processing: %r' % item)
        except KeyError:
            print('Done')
            break


if __name__ == '__main__':
    main()