#!/bin/env python
# -*- coding: utf-8 -*-
import io
import logging
from calender.externals.data import *
import tornado.gen
from calender.common.utils import auth_post, replace_url_bot_no
from tornado.httpclient import AsyncHTTPClient
from calender.constant import API_BO, OPEN_API


LOGGER = logging.getLogger("calender")

"""
type req struct {
    AccountId *string     `json:"accountId,omitempty"`
    RoomId    *string     `json:"roomId,omitempty"`
    Content   interface{} `json:"content"`
}
"""


@tornado.gen.coroutine
def push_message(req, header=None):
    LOGGER.info("detail push_message")
    error_code = False
    headers = API_BO["headers"]
    if header is not None:
        headers = Merge(header, headers)
    headers["consumerKey"] = OPEN_API["consumerKey"]

    url = API_BO["push_url"]
    url = replace_url_bot_no(url)
    if url is None:
        LOGGER.info("user_no is None . url:%s", url)
        return True

    LOGGER.info("push message . url:%s body:%s headers:%s",
                url, str(req), str(headers))
    response = auth_post(url, data=json.dumps(req), headers=headers)
    if response.status_code != 200:
        LOGGER.info("push message failed. url:%s text:%s body:%s",
                    url, response.text, response.content)
        return True
    LOGGER.info("push message success. url:%s txt:%s body:%s",
                url, response.text, response.content)
    return error_code
