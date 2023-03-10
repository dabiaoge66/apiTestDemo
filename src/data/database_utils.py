import pymysql
import yaml
from config.utils import get_project_path, FileEnum
from log.log_utils import get_log


def check_data(data_tuple):
    """
    遍历打印sql查询数据
    :param: 传数据库查询结果（tuple）
    """
    for result in data_tuple:
        print(result)


def read_conf(index, path=FileEnum.DB_CONF.value):
    """
    读配置文件
    :param index: 配置id
    :param path: 配置文件路径
    :return: 返回读取结果
    """
    with open(get_project_path(path), encoding="utf-8", mode="r") as f:
        value = yaml.load(f, yaml.FullLoader)[index]
    return value


class OperateDB:
    def __init__(self):
        """
        连接数据库
        :param: path: 文件路径
        """
        # 日志对象
        self.logger = get_log('database_utils.log', 'r')
        # 取对应索引的配置信息
        data = read_conf(0)
        # 创建数据库对象
        self.db = pymysql.connect(
            host=data["host"],
            user=data["user"],
            password=data["password"],
            charset=data["charset"]
        )
        # 创建游标对象
        self.cursor = self.db.cursor()

    def query_sql(self, sql_str):
        """
        执行查询语句
        :param sql_str: 查询sql
        :return: 查询结果（元组）
        """
        self.logger.debug(f'执行sql语句：{sql_str}')
        self.cursor.execute(sql_str)  # 执行sql
        data_tuple = self.cursor.fetchall()
        return data_tuple

    def execute_sql(self, sql_str):
        """
        执行增删改语句
        :param sql_str: 增删改sql
        :return:
        """
        try:
            self.logger.debug(f'执行sql语句：{sql_str}')
            self.cursor.execute(sql_str)  # 执行sql
            self.db.commit()  # 提交到数据库执行
            # data_tuple = self.cursor.fetchall()
            # return data_tuple
        except pymysql.Error as e:
            self.db.rollback()  # 执行失败则回滚
            self.logger.debug('已回滚')
            self.logger.error(e.args[0], e.args[1])
            raise e

    def exit_db(self):
        """
        # 关闭游标对象和数据库对象
        :return:
        """
        self.cursor.close()
        self.logger.info('游标关闭')
        self.db.close()
        self.logger.info('连接关闭')

    def handle_db(self, sql_str):
        # 根据用例执行相应语句
        if sql_str.startswith('select') or sql_str.startswith('SELECT'):
            data_tuple = self.query_sql(sql_str)
            return data_tuple
        elif sql_str.startswith('update') or sql_str.startswith('UPDATE') or \
                sql_str.startswith('delete') or sql_str.startswith('DELETE'):
            self.execute_sql(sql_str)
        # 关闭游标对象和数据库对象
        self.exit_db()
