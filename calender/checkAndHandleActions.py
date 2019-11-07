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

def check_is_message_time(message):
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
        content_type = ""
        content_post_back = ""
        content = body.get("content", None)
        if content is not None:
            content_type = content.get("type", "")
            content_post_back = content.get("postback", "")
            self.__text = content.get("text", None)

        if type == "postback":
            self.__post_back = body.get("data", "")

        if type == "message" and content_type == "text" \
                and content_post_back == "" \
                and check_is_message_time(self.__text):
            self.code, self.message = yield deal_message(self.__account_id,
                                                         self.__text,
                                                         self.__create_time)

        elif content_post_back == "start":
            self.code, self.message = yield start(self.__account_id)

        elif self.__post_back == "to_first":
            self.code, self.message = to_first(self.__account_id)

        elif self.__post_back == "sign_in":
            self.code, self.message = yield sign_in(self.__account_id,
                                                    self.__current_date)

        elif self.__post_back == "sign_out":
            self.code, self.message = yield sign_out(self.__account_id,
                                                     self.__current_date)

        elif self.__post_back == "direct_sign_in" \
                or content_post_back == "direct_sign_in":
            self.code, self.message = yield direct_sign_in(self.__account_id,
                                                           self.__current_date,
                                                           self.__create_time)

        elif self.__post_back == "direct_sign_out" \
                or content_post_back == "direct_sign_out":
            self.code, self.message = yield direct_sign_out(self.__account_id,
                                                            self.__current_date,
                                                            self.__create_time)

        elif self.__post_back == "manual_sign_in" \
                or content_post_back == "manual_sign_in":
            self.code, self.message = yield  manual_sign_in(self.__account_id,
                                                            self.__current_date)

        elif self.__post_back == "manual_sign_out" \
                or content_post_back == "manual_sign_out":
            self.code, self.message = yield manual_sign_out(self.__account_id,
                                                            self.__current_date)
        elif self.__post_back.find("confirm_in") != -1:
            message = self.__post_back
            if self.__post_back is None:
                message = self.__text
            self.code, self.message = yield confirm_in(self.__account_id,
                                                       self.__current_date,
                                                       message)

        elif self.__post_back.find("confirm_out") != -1:
            message = self.__post_back
            if self.__post_back is None:
                message = self.__text
            self.code, self.message = yield confirm_out(self.__account_id,
                                                        self.__current_date,
                                                        message)
        else:
            self.error_message = "Error \"callback\" type."
        return
