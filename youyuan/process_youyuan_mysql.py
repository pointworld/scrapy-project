import json
import redis
import pymysql.cursors


def main():
    redis_cli = redis.Redis(host='192.168.1.114', port=6379, db=0)
    mysql_cli = pymysql.Connect(
        host='172.16.195.195',
        port=3306,
        user='root',
        password='mysql',
        db='youyuan',
        charset='utf8'
    )

    while True:
        # 将数据从 Redis 里 pop 出来
        source, data = redis_cli.blpop('yy:items')

        item = json.loads(data, encoding='utf-8')

        try:
            with mysql_cli.cursor() as cursor:
                # 创建 MySQL 游标对象，可以执行 MySQL 语句

                sql = "insert into `guangdong_mm_18_25` (`username`, `age`, `avatar`, `album`, `monologue`, `birthplace`, `degree`, `hobby`, `homepage`, `data_source`) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                values = (item["username"], item["age"], item["avatar"], item["album"], item["monologue"],
                          item["birthplace"], item["degree"], item["hobby"], item["homepage"],
                          item["data_source"])

                cursor.execute(sql, values)

                # 提交事务
                mysql_cli.commit()

        except Exception as e:
            print('*' * 50)
            print(e)
            mysql_cli.close()


if __name__ == '__main__':
    main()
