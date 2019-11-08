#!/bin/env python
# -*- coding: utf-8 -*-
import time
import logging
import tornado.web
from calender.actions.start import start
from calender.actions.to_first import to_first
from calender.actions.sign_in import sign_in
from calender.actions.sign_out import sign_out
from calender.actions.direct_sign_in import direct_sign_in
from calender.actions.direct_sign_out import direct_sign_out
from calender.actions.manual_sign_in import manual_sign_in
from calender.actions.manual_sign_out import manual_sign_out
from calender.actions.deal_message import deal_message
from calender.actions.confirm_in import confirm_in
from calender.actions.confirm_out import confirm_out

LOGGER = logging.getLogger("calender")

cmd_message = ["start", "clean"]

def is_message_time(message):
    if message is None or message in cmd_message \
            or message.find("confirm_out") != -1 \
            or message.find("confirm_in") != -1:
        return False
    return True


class CheckAndHandleActions:
    __text = ""
    __post_back = ""
    __account_id = None
    code = None
    message = None
    __create_time = None
    __current_date = None
    __content_type = ""
    __content_post_back = ""
    __handle = None
    __user_message = None

    def __init__(self):
        self.__create_time = time.time()
        self.__current_date = time.strftime("%Y-%m-%d",
                                            time.localtime(self.__create_time))

    @tornado.gen.coroutine
    def execute(self, body):

        if body is None or "source" not in body or "accountId" \
                not in body["source"]:
            self.message = "can't find \"accountId\" field."
            return
        if "type" not in body:
            self.message = "can't find \"type\" field."
            return

        self.__account_id = body["source"].get("accountId", None)

        if self.__account_id is None:
            self.message = "\"accountId\" is None."
            return

        type = body.get("type", "")
        
        content = body.get("content", None)
        if content is not None:
            self.__content_type = content.get("type", "")
            self.__content_post_back = content.get("postback", "")
            self.__text = content.get("text", None)

        if type == "postback":
            self.__post_back = body.get("data", "")

        if type == "message" and self.__content_type == "text" \
                and self.__content_post_back == "" \
                and is_message_time(self.__text):
            self.__user_message = self.__text
            self.__handle = deal_message

        elif self.__content_post_back == "start":
            self.__handle = start

        elif self.__post_back == "to_first":
            self.__handle = to_first

        elif self.__post_back == "sign_in":
            self.__handle = sign_in

        elif self.__post_back == "sign_out":
            self.__handle = sign_out

        elif self.__post_back == "direct_sign_in" \
                or self.__content_post_back == "direct_sign_in":
            self.__handle = direct_sign_in

        elif self.__post_back == "direct_sign_out" \
                or self.__content_post_back == "direct_sign_out":
            self.__handle = direct_sign_out

        elif self.__post_back == "manual_sign_in" \
                or self.__content_post_back == "manual_sign_in":
            self.__handle = manual_sign_in

        elif self.__post_back == "manual_sign_out" \
                or self.__content_post_back == "manual_sign_out":
            self.__handle = manual_sign_out

        elif self.__post_back.find("confirm_in") != -1:
            self.__user_message = self.__post_back
            if self.__post_back is None:
                self.__user_message = self.__text
            self.__handle = confirm_in

        elif self.__post_back.find("confirm_out") != -1:
            self.__user_message = self.__post_back
            if self.__post_back is None:
                self.__user_message = self.__text
            self.__handle = confirm_out

        if self.__handle is not None:
            self.code, self.message = yield self.__handle(self.__account_id,
                                                          self.__current_date,
                                                          self.__create_time,
                                                          self.__user_message)
        else:
            self.error_message = "Error \"callback\" type."
        return
