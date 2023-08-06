# -*- coding: UTF-8 -*-
import traceback

from sppush.sdk import PushSDK
from sppush.sdk import RequestException
from conf import HOST
from conf import APPKEY
from conf import MASTERSECRET

push_client = PushSDK(HOST, APPKEY, MASTERSECRET)


def push_msg_delete():
    msg = {
        "msg_id": "2001",
    }
    try:
        result = push_client.delete(msg)
        print(result)
    except RequestException as e:
        traceback.print_exc(e)
    except Exception as e:
        traceback.print_exc(e)


if __name__ == '__main__':
    push_msg_delete()
