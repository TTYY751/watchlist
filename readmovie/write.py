import sqlite3

# 传入数据库文件路径
db_file_path = 'C:/Users/飞行堡垒/Desktop/watchlist/readmovie/movieDB.db'


def read_sqlite_db(db_file_path):
    # 连接到 SQLite 数据库
    connection = sqlite3.connect(db_file_path)

    # 创建游标对象
    cursor = connection.cursor()

    # 执行 SQL 查询语句
    cursor.execute("SELECT * FROM movie_actor_relation")

    # 获取查询结果
    rows = cursor.fetchall()

    # 打印查询结果
    for row in rows:
        print(row)

    # 关闭连接
    connection.close()


# 调用函数读取并打印数据库内容
read_sqlite_db(db_file_path)
