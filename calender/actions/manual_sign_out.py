#!/bin/env python
# -*- coding: utf-8 -*-
import tornado.web
import asyncio
import logging
from calender.model.data import i18n_text, make_text
from calender.externals.send_message import push_messages
from calender.actions.message import invalid_message, prompt_input
from calender.model.processStatusDBHandle import get_status_by_user, \
    set_status_by_user_date

LOGGER = logging.getLogger("calender")


def manual_sign_out_message():
    jp_text = i18n_text("ja_JP", "退勤時間を直接入力してください。")
    en_text = i18n_text("en_US", "Please manually enter the clock-out time.")
    kr_text = i18n_text("ko_KR", "퇴근 시간을 직접 입력해 주세요. ")

    i18n_texts1 = [jp_text, en_text, kr_text]

    text1 = make_text("퇴근 시간을 직접 입력해 주세요. ", i18n_texts1)

    text2 = prompt_input()

    return [text1, text2]


@tornado.gen.coroutine
def manual_sign_out_content(account_id, current_date):

    yield asyncio.sleep(1)
    content = get_status_by_user(account_id, current_date)

    if content is None or content[1] is None or content[1] != "sign_in_done":
        return [invalid_message()]

    set_status_by_user_date(account_id, current_date, "wait_out")

    return manual_sign_out_message()


@tornado.gen.coroutine
def manual_sign_out(account_id, current_date, _, __):
    contents = yield manual_sign_out_content(account_id, current_date)

    yield push_messages(account_id, contents)
