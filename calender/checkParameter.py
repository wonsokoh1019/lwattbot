#!/bin/env python
# -*- coding: utf-8 -*-
from enum import Enum


cmd_message = ["start", "manual_sign_out", "manual_sign_in",
               "direct_sign_out", "direct_sign_in", "sign_out",
               "sign_in", "clean"]


def check_is_message_time(message):
    if message is None or message in cmd_message \
            or message.find("confirm_out") != -1 \
            or message.find("confirm_in") != -1:
        return False
    return True


class UserCmd(Enum):
    DEFAULT = 0
    START = 1
    SIGN_IN = 2
    SIGN_OUT = 3
    DIRECT_SIGN_IN = 4
    DIRECT_SIGN_OUT = 5
    MANUAL_SIGN_IN = 6
    MANUAL_SIGN_OUT = 7
    CONFIRM_IN = 8
    CONFIRM_OUT = 9
    MESSAGE = 10
    CLEAN = 11
    TO_FIRST = 12


class CheckParameter:
    cmd = UserCmd.DEFAULT
    text = ""
    post_back = ""
    account_id = None
    room_id = None
    error_message = None

    def __init__(self, body):
        if body is None or "source" not in body or "accountId" \
                not in body["source"]:
            self.error_message = "can't find \"accountId\" field."
            self.cmd = UserCmd.DEFAULT
            return
        if "type" not in body:
            self.error_message = "can't find \"type\" field."
            self.cmd = UserCmd.DEFAULT
            return

        self.account_id = body["source"].get("accountId", None)
        self.room_id = body["source"].get("roomId", None)

        if self.account_id is None:
            self.error_message = "\"accountId\" is None."
            self.cmd = UserCmd.DEFAULT
            return

        type = body.get("type", "")
        content_type = ""
        content_post_back = ""
        content = body.get("content", None)
        if content is not None:
            content_type = content.get("type", "")
            content_post_back = content.get("postback", "")
            self.text = content.get("text", None)

        if type == "postback":
            self.post_back = body.get("data", "")

        if type == "message" and content_type == "text" \
                and content_post_back == "" \
                and check_is_message_time(self.text):
            self.cmd = UserCmd.MESSAGE
        elif content_post_back == "start" or self.text == "start":
            self.cmd = UserCmd.START
        elif content_post_back == "clean" or self.text == "clean":
            self.cmd = UserCmd.CLEAN
        elif self.post_back == "to_first" or self.text == "to_first":
            self.cmd = UserCmd.TO_FIRST
        elif self.post_back == "sign_in" or self.text == "sign_in":
            self.cmd = UserCmd.SIGN_IN
        elif self.post_back == "sign_out" or self.text == "sign_out":
            self.cmd = UserCmd.SIGN_OUT
        elif self.post_back == "direct_sign_in" \
                or self.text == "direct_sign_in" \
                or content_post_back == "direct_sign_in":
            self.cmd = UserCmd.DIRECT_SIGN_IN
        elif self.post_back == "direct_sign_out" \
                or self.text == "direct_sign_out" \
                or content_post_back == "direct_sign_out":
            self.cmd = UserCmd.DIRECT_SIGN_OUT
        elif self.post_back == "manual_sign_in" \
                or self.text == "manual_sign_in" \
                or content_post_back == "manual_sign_in":
            self.cmd = UserCmd.MANUAL_SIGN_IN
        elif self.post_back == "manual_sign_out" \
                or self.text == "manual_sign_out" \
                or content_post_back == "manual_sign_out":
            self.cmd = UserCmd.MANUAL_SIGN_OUT
        elif self.post_back.find("confirm_in") != -1 \
                or self.text.find("confirm_in") != -1:
            self.cmd = UserCmd.CONFIRM_IN
        elif self.post_back.find("confirm_out") != -1 \
                or self.text.find("confirm_out") != -1:
            self.cmd = UserCmd.CONFIRM_OUT
        else:
            self.error_message = "Error \"callback\" type."
            self.cmd = UserCmd.DEFAULT
        return
