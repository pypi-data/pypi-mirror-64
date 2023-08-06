# -*- coding: utf8 -*-
import MySQLdb
import time
import traceback


class StoreMysql(object):
    """
    mysql读写相关操作，需安装MySQLdb库
    Args:
        host:数据库ip
        user:数据库用户名
        password:数据库用户密码
        db:数据库名
        port:数据库端口，默认3306
        max_idle_time:数据库连接维持时间
        connect_timeout:连接超时时间
        charset:数据库编码，默认utf8
    """
    def __init__(self, host="", user="", password="", db="", port=3306, max_idle_time=7*3600, connect_timeout=30,
                 reconnect_interval=5, reconnect_times=12, charset="utf8", defer_warnings=False):
        self.host = host
        self.db = db
        self.max_idle_time = float(max_idle_time)
        self.reconnect_interval = reconnect_interval
        self.reconnect_times = reconnect_times
        self.defer_warnings = defer_warnings
        args = dict(host=host, user=user, passwd=password, port=port, db=db,
                    use_unicode=True, charset=charset, init_command='SET names utf8',
                    connect_timeout=connect_timeout)

        self._db = None
        self._db_args = args
        self._last_use_time = time.time()
        try:
            self.reconnect()
        except Exception:
            print("Cannot connect to MySQL on %s" % self.host)

    def __del__(self):
        self.close()

    def close(self):
        if getattr(self, "_db", None) is not None:
            self._db.close()
            self._db = None

    def reconnect(self):
        self.close()
        try:
            self._db = MySQLdb.connect(**self._db_args)
        except Exception:
            time.sleep(self.reconnect_interval)

    def _ensure_connected(self):
        if time.time() - self._last_use_time > self.max_idle_time:
            self.close()
        try_time = 0
        while self._db is None and try_time < self.reconnect_times:
            self.reconnect()
            try_time += 1
        self._last_use_time = time.time()

    def _cursor(self):
        self._ensure_connected()
        cursor = self._db.cursor()
        if self.defer_warnings:
            cursor._defer_warnings = True
        return cursor

    def query(self, sql):
        """
        根据sql查询
        Returns：
            数组的数组，外层数组元素为一行，内存数组元素为一行的一列
        """
        rows = []
        cur = self._cursor()
        try:
            cur.execute(sql)
            self._db.commit()
            rows = cur.fetchall()
        except MySQLdb.OperationalError as e:
            print("Error connecting to MySQL on %s" % self.host)
            traceback.print_exc()
            self.close()
        except Exception as e:
            print("mysql query exception:" + sql)
            traceback.print_exc()
        finally:
            cur.close()
        return rows

    def count(self, tb):
        """
        返回某表的行数
        Args:
            tb:字符串，表名称
        """
        sql = 'select count(*) from %s' %(tb)
        results = self.query(sql)
        if len(results) == 1 and len(results[0]) == 1:
            return int(results[0][0])

    def do(self, sql, flag='lastrowid'):
        """
        执行sql，insert/delete/update操作
        Args:
            sql:要执行的sql
            flag:返回值类型，flag=lastrowid返回lastrowid，flag=rowcount返回rowcount
        """
        cur = self._cursor()
        try:
            cur.execute(sql)
            self._db.commit()
            if flag == 'lastrowid':
                return cur.lastrowid
            elif flag == 'rowcount':
                return cur.rowcount
            return 1
        except MySQLdb.OperationalError as e:
            print("Error connecting to MySQL on %s" % self.host)
            traceback.print_exc()
            self.close()
            return -1
        except Exception as e:
            print("mysql execute exception:" + sql)
            traceback.print_exc()
            return -1
        finally:
            cur.close()

    def save(self, table, data):
        """
        将字典直接insert到数据库
        Args:
            table:字符串，插入目标表的名称
            data:字典格式，key为字段名称，value为字段值，如{'id':'1','name':'temp'}
        """
        if len(data) == 0:
            return -1
        try:
            fields, values = zip(*data.items())
            if len(fields) == 0 or len(values) == 0:
                return -1
            return self.do("insert ignore into %s(`%s`) values('%s')" \
                           % (table, '`, `'.join(fields), "', '".join(MySQLdb.escape_string(str(value)) for value in values)))
        except Exception as e:
            traceback.print_exc()
            return -1

    def update(self, table, data, field):
        """
        将字典直接update到数据库
        Args:
            table:字符串，更新目标表的名称
            data:字典格式，key为字段名称，value为字段值，如{'id':'1','name':'temp'}
            field:唯一索引字段，即根据该字段判断是否为同一条记录，作为where条件
        """
        if len(data) == 0:
            return -1
        try:
            if field not in data:
                return -1
            values = []
            for key, value in data.items():
                values.append("`%s` = '%s'" % (key, MySQLdb.escape_string(str(value))))
            if len(values) == 0:
                return -1
            return self.do("update %s set %s where `%s` = '%s'" % (table, ','.join(values), field, MySQLdb.escape_string(str(data[field]))), flag='rowcount')
        except Exception as e:
            traceback.print_exc()
            return -1

    def save_or_update(self, table, data, field):
        """
        将字典更新到数据库，如果已存在则update，不存在则insert
        Args:
            table:字符串，更新目标表的名称
            data:字典格式，key为字段名称，value为字段值，如{'id':'1','name':'temp'}
            field:唯一索引字段，即根据词字段判断是否为同一条记录，作为where条件
        """
        if len(data) == 0:
            return -1
        try:
            if field not in data:
                return -1
            rows = self.query("select count(1) from %s where `%s` = '%s'" % (table, field, MySQLdb.escape_string(str(data[field]))))
            if rows and rows[0][0] > 0:
                return self.update(table, data, field)
            else:
                return self.save(table, data)
        except Exception as e:
            traceback.print_exc()
            return -1
