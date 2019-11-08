#!/bin/env python
# -*- coding: utf-8 -*-
import tornado.web
import asyncio
import logging
from calender.model.data import i18n_text, make_text
from calender.externals.send_message import push_messages
from calender.actions.message import invalid_message, prompt_input
from calender.model.processStatusDBHandle import get_status_by_user, \
    insert_replace_status_by_user_date

LOGGER = logging.getLogger("calender")


def manual_sign_in_message():
    jp_text = i18n_text("ja_JP", "出勤時間を直接入力してください。")
    en_text = i18n_text("en_US", "Please manually enter the clock-in time.")
    kr_text = i18n_text("ko_KR", "출근 시간을 직접 입력해 주세요. ")

    i18n_texts1 = [jp_text, en_text, kr_text]

    text1 = make_text("출근 시간을 직접 입력해 주세요. ", i18n_texts1)

    text2 = prompt_input()

    return [text1, text2]


@tornado.gen.coroutine
def manual_sign_in_content(account_id, current_date):
    yield asyncio.sleep(1)

    content = get_status_by_user(account_id, current_date)

    if content is not None and content[1] is not None:
        return [invalid_message()]

    insert_replace_status_by_user_date(account_id, current_date, "wait_in")

    return manual_sign_in_message()


@tornado.gen.coroutine
def manual_sign_in(account_id, current_date, _, __):
    contents = yield manual_sign_in_content(account_id, current_date)
    if contents is None:
        return False, "manual sign in. content is None"
    success_code, error_message = yield push_messages(account_id, contents)
    return success_code, error_message
