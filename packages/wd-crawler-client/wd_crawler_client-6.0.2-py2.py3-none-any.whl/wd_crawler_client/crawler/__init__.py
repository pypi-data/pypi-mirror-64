# -*- coding: utf-8 -*-
import logging
import json
import random

from treq import post
from twisted.internet import defer, reactor, task
from twisted.web import http
from twisted.web.client import HTTPConnectionPool

from wd_crawler_client.lib.md5 import MD5
from wd_crawler_client.lib.queue import DiskQueue, PriorityQueue


class Request(object):

    def __init__(self, task_id, url, headers, data=None, redirect=None, verify=None, is_head=None, return_header=None,
                 encoding=None, timeout=None, retry_times=None, extract_type=None, priority=2, md5_suffix='', **kwargs):
        """
        Request对象
        :param task_id: str，任务id
        :param url: str，待抓取URL
        :param headers: dict，请求头
        :param data: str，请求数据，POST请求有效
        :param redirect: int，是否支持跳转，默认支持(1)
        :param verify: int，是否做https验证，默认支持(1)
        :param is_head: int，是否发送HEAD请求，默认不发送(0)
        :param return_header: int，是否返回响应头，默认不返回(0)
        :param encoding: str，页面编码，默认不指定
        :param timeout: int，超时时间，默认30s
        :param retry_times: int，抓取失败重试，默认3
        :param extract_type: int，解析类型：0->不解析;1->解析百度PC排名结果;2->解析百度移动排名结果;3->解析百度真实URL;
                                            4->解析百度PC URL是否收录;5->解析360PC排名结果;6->解析360移动排名结果;
                                            7->解析搜狗PC排名结果;8->解析搜狗移动排名结果;9->解析网页TDK
        :param priority: int，优先级：2->中;3->高
        :param kwargs: 其他参数
        """
        assert task_id is not None, "%s must have a task_id" % type(self).__name__
        assert url is not None, "%s must have a url" % type(self).__name__
        self.tid = task_id
        self.url = url
        self.uid = MD5.md5(url + md5_suffix)
        self.headers = headers
        self.data = data
        self.redirect = redirect
        self.verify = verify
        self.is_head = is_head
        self.return_header = return_header
        self.encoding = encoding
        self.timeout = timeout
        self.retry_times = retry_times
        self.extract_type = extract_type
        self.priority = priority
        self.__dict__.update(kwargs)

    @property
    def params(self):
        request = {'tid': self.tid, 'uid': self.uid, 'u': self.url, 'hs': self.headers}
        if self.data is not None:
            request['d'] = self.data
        if self.redirect is not None:
            request['r'] = self.redirect
        if self.verify is not None:
            request['v'] = self.verify
        if self.is_head is not None:
            request['ih'] = self.is_head
        if self.return_header is not None:
            request['rh'] = self.return_header
        if self.timeout is not None:
            request['t'] = self.timeout
        if self.retry_times is not None:
            request['rt'] = self.retry_times
        if self.encoding is not None:
            request['e'] = self.encoding
        if self.extract_type is not None:
            request['et'] = self.extract_type
        if self.priority is not None:
            request['pr'] = self.priority
        return json.dumps(request)


class Crawler(object):

    # test
    # server = 'http://127.0.0.1:12000'

    # nginx online
    server = 'http://118.89.92.123:11010'

    def __init__(self, user_id, name, priority=2, db_params=None, user_agents=None):
        assert user_id is not None, "%s must have user_id" % type(self).__user_id__
        self.user_id = user_id
        assert name is not None, "%s must have a name" % type(self).__name__
        self.name = name
        self.task_id = None
        self.priority = priority
        self.pool = HTTPConnectionPool(reactor)
        if db_params:
            from twisted.enterprise import adbapi
            self.dbPool = adbapi.ConnectionPool("MySQLdb", cp_reconnect=True, use_unicode=True, charset='utf8',
                                                init_command='SET names utf8', connect_timeout=30, **db_params)
        if user_agents:
            self.user_agents = user_agents
        else:
            from wd_crawler_client.lib.user_agents import UA_PC
            self.user_agents = UA_PC
        self.queue = PriorityQueue(DiskQueue, [1, 2, 3], path='tmp/%s' % self.name)
        self.requests = {}
        self.max_requests = 300
        logging.basicConfig(filename='logs/%s.log' % self.name, level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(name)s : %(message)s')
        self.logger = logging.getLogger('spider')

    @defer.inlineCallbacks
    def start(self):
        success = False
        try:
            response = yield post('%s/connect/' % self.server, data={
                'user_id': self.user_id, 'name': self.name, 'priority': self.priority}, pool=self.pool)
            msg = yield response.text()
            self.log('connect resp: ' + msg, logging.INFO)
            if response.code == http.OK:
                result = yield response.json()
                if result['success']:
                    success = True
                    self.log('connect success, start fetching ...')
                    self.task_id = result['task_id']
                    yield defer.maybeDeferred(self.init_requests)
                    task.LoopingCall(self.fetch).start(2)
                else:
                    self.log('connect failure: ' + result['message'], logging.ERROR)
            else:
                message = yield response.text()
                self.log('connect error: ' + message, logging.ERROR)
        except Exception as e:
            success = False
            import traceback
            traceback.print_exc()
            self.log('connect error: ' + str(e), logging.ERROR)
        finally:
            if not success:
                self.stop()

    def init_requests(self):
        raise NotImplementedError

    def make_request(self, url, headers=None, data=None, redirect=None, verify=None, is_head=None, return_header=None,
                     encoding=None, timeout=None, retry_times=None, extract_type=None, priority=2, md5_suffix='',
                     **kwargs):
        request = Request(self.task_id, url, headers or {'User-Agent': random.choice(self.user_agents)}, data, redirect,
                          verify, is_head, return_header, encoding, timeout, retry_times, extract_type, priority,
                          md5_suffix, **kwargs)
        self.queue.put(request, priority)

    def fetch(self):
        if len(self.requests) == 0 and len(self.queue) == 0:
            self.stop()
        else:
            requests = []
            for _ in range(self.max_requests - len(self.requests)):
                if len(self.queue):
                    request = self.queue.get()
                    requests.append(request)
                    self.requests[request.uid] = request
                else:
                    break
            if requests:
                self.send(requests)
            for _ in range(int(len(self.requests)/100) + 1):
                self.get()

    @defer.inlineCallbacks
    def send(self, requests):
        success = False
        try:
            self.log('send request reqs len:%d' % (len(requests)), logging.INFO)

            response = yield post(
                '%s/task/' % self.server,
                {'task_id': self.task_id, 'urls': json.dumps([request.params for request in requests])}, pool=self.pool)
            if response.code == http.OK:
                success = True
        except Exception as e:
            self.log('send request error: ' + str(e), logging.ERROR)
        finally:
            if not success:
                for request in requests:
                    self.queue.put(request, 3)

    @defer.inlineCallbacks
    def get(self):
        try:
            response = yield post('%s/result/' % self.server, {'task_id': self.task_id}, pool=self.pool)
            if response.code == http.OK:
                response = yield response.json()
                if response['success']:
                    for result in response['results']:
                        try:
                            result = json.loads(result)
                        except:
                            continue
                        if result['uid'] in self.requests:
                            request = self.requests[result['uid']]
                            if 'success' not in result:
                                self.queue.put(request, 3)
                            else:
                                try:
                                    yield defer.maybeDeferred(self.deal, result, request)
                                    self.requests.pop(result['uid'], None)
                                except Exception as e1:
                                    self.log('deal error: ' + str(e1), logging.ERROR)
                                    import traceback
                                    traceback.print_exc()
        except Exception as e:
            self.log('get result error: ' + str(e), logging.ERROR)

    def deal(self, response, request):
        raise NotImplementedError

    def finished(self, success):
        pass

    @defer.inlineCallbacks
    def stop(self, success=True):
        try:
            if self.task_id:
                response = yield post('%s/disconnect/' % self.server, data={'task_id': self.task_id}, pool=self.pool)
                self.log('disconnect resp.code: %d' % (response.code), logging.INFO)
                if response.code == http.OK:
                    result = yield response.json()
                    self.log('disconnect resp:%s' % (result), logging.INFO)
                    if result['success']:
                        self.log('disconnect success, stop fetching ...')
                    else:
                        self.log('disconnect failure: ' + result['message'], logging.ERROR)
                else:
                    message = yield response.text()
                    self.log('disconnect error: ' + message, logging.ERROR)
            yield defer.maybeDeferred(self.finished, success)
        except Exception as e:
            self.log('disconnect error: ' + str(e), logging.ERROR)
        finally:
            reactor.stop()

    def run(self):
        reactor.callWhenRunning(self.start)
        reactor.run()

    def log(self, message, level=logging.DEBUG, **kw):
        self.logger.log(level, message, **kw)

    @staticmethod
    def interaction(cursor, sql, flag='count', defer_warnings=True):
        cursor._cursor._defer_warnings = defer_warnings
        ret = cursor.execute(sql)
        if flag == 'id':
            return cursor.lastrowid
        return cursor.rowcount

    @defer.inlineCallbacks
    def insert(self, table, data):
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
            sql = "insert into %s(`%s`) values('%s')" % (table, 
                    '`, `'.join(fields),
                    "', '".join(str(value) for value in values))
            ret = yield self.dbPool.runInteraction(self.interaction, sql, 'id')
            return 0
        except Exception as e:
            import traceback
            traceback.print_exc()
            return -1

    @defer.inlineCallbacks
    def insert_many(self, table, datas):
        for data in datas:
            ret = yield self.insert(table, data)
            if ret == -1:
                return ret
        return 0

    @defer.inlineCallbacks
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
                values.append("`%s` = '%s'" % (key, str(value)))
            if len(values) == 0:
                return -1
            sql = "update %s set %s where `%s` = '%s'" % (table, ','.join(values), field, str(data[field]))
            yield self.dbPool.runInteraction(self.interaction, sql)
            return 0
        except Exception as e:
            import traceback
            traceback.print_exc()
            return -1

    @defer.inlineCallbacks
    def update_many(self, table, datas, field):
        for data in datas:
            ret = yield self.update(table, data, field)
            if ret == -1:
                return ret
        return 0


class CaptureCrawler(Crawler):

    def __init__(self, name, priority=2, db_params=None, user_agents=None):
        self.server = 'http://10.105.47.191:21010'
        super(CaptureCrawler, self).__init__(name, priority, db_params, user_agents)
