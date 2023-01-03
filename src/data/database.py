import pymysql


def handle_database(sql_str):
    """
    数据库操作
    :param: 传sql
    """
    db = pymysql.connect(host="192.168.1.6", user='tob', password='tob_lmb@123')
    cursor = db.cursor()

    try:
        cursor.execute(sql_str)  # 执行sql
        db.commit()  # 提交到数据库执行
        data_tuple = cursor.fetchall()
        return data_tuple

    except pymysql.Error as e:
        db.rollback()  # 执行失败则回滚
        print(e.args[0], e.args[1])
    finally:
        cursor.close()
        db.close()


def check_data(data_tuple):
    """
    遍历打印sql查询数据
    :param: 传数据库查询结果（tuple）
    """
    for result in data_tuple:
        print(result)
