import sqlite3


def execute_sql_from_file(sql_file, database_file):
    # 连接到 SQLite 数据库
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()

    try:
        # 读取 SQL 文件中的语句并执行
        with open(sql_file, 'r', encoding='utf-8') as file:
            sql_statements = file.read().split(';')
            for statement in sql_statements:
                if statement.strip():
                    cursor.execute(statement)

        # 提交并保存更改
        connection.commit()
        print(f"SQL statements from '{sql_file}' executed successfully.")
    except sqlite3.Error as e:
        print(f"Error executing SQL statements: {e}")
    finally:
        # 关闭连接
        connection.close()


# 指定 SQL 文件和目标数据库文件
sql_file_path = 'C:/Users/飞行堡垒/Desktop/watchlist/readmovie/movie.txt'  # 替换为实际的 SQL 文件路径
database_file_path = 'C:/Users/飞行堡垒/Desktop/watchlist/readmovie/movieDB.db'  # 替换为实际的数据库文件路径

# 执行 SQL 语句
execute_sql_from_file(sql_file_path, database_file_path)
