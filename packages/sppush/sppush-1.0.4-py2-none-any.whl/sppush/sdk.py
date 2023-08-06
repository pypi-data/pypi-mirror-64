# -*- coding: UTF-8 -*-
################################################################################
#
# Copyright (c) 2018 Baidu.com, Inc. All Rights Reserved
#
################################################################################

import datetime
import hashlib
import json
import logging
import time
import requests
from six.moves.urllib.parse import quote_plus

logger_name = "sppush"
logger = logging.getLogger(logger_name)

SDK_VERSION = "1.0.4"
DEFAULT_HOST = "https://push.safe.baidu.com/"
DEFAULT_TIMEOUT = 30


def gen_sign(method, url, data_json, appkey, timestamp, master_secret):
    """
    生成签名
    :param method:
    :param url:
    :param data_json:
    :param appkey:
    :param timestamp:
    :param master_secret:
    :return:
    """
    raw = '%s%s%s%s%s%s' % (method, url, data_json, appkey, timestamp, master_secret)
    url_raw = quote_plus(raw)
    return hashlib.md5(url_raw.encode('utf-8')).hexdigest()


class PushSDK:
    session = requests.session()
    timeout = DEFAULT_TIMEOUT
    host = DEFAULT_HOST
    version = SDK_VERSION

    def __init__(self, host, appkey, master_secret, timeout=None):
        """
        初始化sdk
        :param host:
        :param appkey:
        :param master_secret:
        """
        self.appkey = appkey
        self.host = host
        self.master_secret = master_secret

        if timeout is None:
            self.timeout = DEFAULT_TIMEOUT
        else:
            self.timeout = timeout

    def set_logging(self, level):
        level_list = ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"]
        if level in level_list:
            if level == "CRITICAL":
                logging.basicConfig(level=logging.CRITICAL)
            if level == "ERROR":
                logging.basicConfig(level=logging.ERROR)
            if level == "WARNING":
                logging.basicConfig(level=logging.WARNING)
            if level == "INFO":
                logging.basicConfig(level=logging.INFO)
            if level == "DEBUG":
                logging.basicConfig(level=logging.DEBUG)
            if level == "NOTSET":
                logging.basicConfig(level=logging.NOTSET)
        else:
            print ("set logging level failed ,the level is invalid.")

    def http_post(self, url, params):
        """
        发送请求
        :param url:
        :param params:
        :return:
        """
        headers = dict()
        data_json = json.dumps(params)
        appkey = self.appkey
        master_secret = self.master_secret
        method = 'POST'
        timestamp = int(time.mktime(datetime.datetime.utcnow().timetuple()))
        sign = gen_sign(method, url, data_json, appkey, timestamp, master_secret)
        url = '%s?appkey=%s&timestamp=%s&sign=%s' % (url, appkey, timestamp, sign)
        logger.debug("request url : %s", url)
        logger.debug("request body : %s", data_json)
        try:
            resp = self.session.post(
                url,
                data=data_json,
                headers=headers,
                timeout=self.timeout,
                verify=True,
                stream=False
            )
        except Exception as e:
            # traceback.print_exc(e)
            raise RequestException('request sppush server error : %s' % e.message)

        resp_str = resp.text
        logger.debug("resp : %s", resp_str)
        resp_obj = json.loads(resp_str)
        return resp_obj

    def unicast(self, message):
        """
        指定1个push_uid下发消息
        :param message:
        :return:
        """
        url = self.host + "push/api/open/v1/message/unicast"
        return self.http_post(url, message)

    def multicast(self, message):
        """
        指定多个push_uid下发消息
        :param message:
        :return:
        """
        url = self.host + "push/api/open/v1/message/multicast"
        return self.http_post(url, message)

    def cuids(self, message):
        """
        指定多个cuid下发消息
        :param message:
        :return:
        """
        url = self.host + "push/api/open/v1/message/cuids"
        return self.http_post(url, message)

    def broadcast(self, message):
        """
        广播消息
        :param message:
        :return:
        """
        url = self.host + "push/api/open/v1/message/broadcast"
        return self.http_post(url, message)

    def delete(self, message):
        """
        删除消息
        :param message:
        :return:
        """
        url = self.host + "push/api/open/v1/message/delete"
        return self.http_post(url, message)


class RequestException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
