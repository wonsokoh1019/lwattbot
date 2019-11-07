#!/bin/env python
# -*- coding: utf-8 -*-
import io
import logging
import json
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
def push_message(account_id, content, header=None):

    if account_id is None:
        return False, "account_id is None."
    if content is None:
        return False, "content is None."

    request = {
        "accountId": account_id,
        "content": content
    }

    headers = API_BO["headers"]
    if header is not None:
        headers = Merge(header, headers)

    headers["consumerKey"] = OPEN_API["consumerKey"]

    url = API_BO["push_url"]
    url = replace_url_bot_no(url)

    if url is None:
        LOGGER.info("user_no is None . body:%s", str(request))
        return False, "push message failed. url is None"

    response = auth_post(url, data=json.dumps(request), headers=headers)
    if response.status_code != 200:
        LOGGER.info("push message failed. url:%s text:%s body:%s",
                    url, response.text, response.content)
        return False, "push message failed."
    return True, None


@tornado.gen.coroutine
def push_messages(account_id, contents):

    if account_id is None:
        return False, "account_id is None."
    if contents is None:
        return False, "contents is None."

    for content in contents:
        error_code, error_message = yield push_message(account_id, content)
        if not error_code:
            LOGGER.info("yield send message failed. account_id:%s",
                        str(account_id))
            return False, error_message
    return True, None
