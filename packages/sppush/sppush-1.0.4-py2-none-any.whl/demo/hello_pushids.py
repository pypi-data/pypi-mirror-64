# -*- coding: UTF-8 -*-
import traceback

from sppush.sdk import PushSDK
from sppush.sdk import RequestException
from conf import HOST
from conf import APPKEY
from conf import MASTERSECRET

push_client = PushSDK(HOST, APPKEY, MASTERSECRET)

# 消息体,对应open-api文档
app_msg = {
    # 0 : 通知 , 2 : 透传
    "message_type": 2,
    # 透传
    "transmission": {
        # 标题
        "title": "title",
        # 内容
        "content": "content",
    },
    # 通知
    "notification": {
        # 标题
        "title": "title",
        # 内容
        "content": "content",
        # 样式
        "style": 5,  # 原生
        # 点击行为
        "action": {
            "action_type": 6,  # 打开应用
        },
        "notify": {
            # 声音  , 0 : 关闭 , 1 : 打开
            "sound": 1,
            # 呼吸灯 , 0 : 关闭 , 1 : 打开
            "lights": 1,
            # 振动 , 0 : 关闭 , 1 : 打开
            "vibrate": 1,
        },
    },
    # 选项
    "option": {
        # 有效时间
        "expire": 3600 * 24,
        # 下发速率
        "speed": 1000,
    },
    # 使用条件筛选
    "condition": [
        {"key": "tags", "values": ["tag1", "tag2"], "operate": "or"},  # 标签筛选
        {"key": "alias", "values": ["alias1", "alias2"], "operate": "or"},  # 别名筛选
    ],
}


def push_msg_unicast():
    unicast_msg = app_msg.copy()
    unicast_msg['push_id'] = "push_id1"
    try:
        result = push_client.unicast(unicast_msg)
        print(result)
    except RequestException, e:
        traceback.print_exc(e)
        return None


def push_msg_multicast():
    multicast_msg = app_msg.copy()
    multicast_msg['push_ids'] = ["push_id1", "push_id2"]
    try:
        result = push_client.multicast(multicast_msg)
        print(result)
    except RequestException as e:
        traceback.print_exc(e)
    except Exception as e:
        traceback.print_exc(e)


if __name__ == '__main__':
    push_msg_unicast()
    push_msg_multicast()
