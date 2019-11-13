# !/bin/env python
# -*- coding: utf-8 -*-
import tornado.web
import logging
from calender.model.data import make_i18n_content_texts, make_button
from calender.externals.send_message import push_message
from calender.actions.message import reminder_message, create_button_actions
from calender.model.processStatusDBHandle import delete_status_by_user_date, \
    get_status_by_user

LOGGER = logging.getLogger("calender")


def sign_in_message():
    jp_text = make_i18n_content_texts("ja_JP", "出勤時間の入力方式"
                                               "を選択してください。")
    en_text = make_i18n_content_texts("en_US", "Register current "
                                               "time as clock-in time")
    kr_text = make_i18n_content_texts("ko_KR", "출근 시간 입력 "
                                               "방식을 선택해 주세요.")
    content_texts = [jp_text, en_text, kr_text]

    actions = create_button_actions("direct_sign_in", "manual_sign_in")

    return make_button("출근 시간 입력 방식을 선택해 주세요.",
                       actions, content_texts=content_texts)


@tornado.gen.coroutine
def sign_in_content(account_id, current_date):

    content = get_status_by_user(account_id, current_date)
    process = None
    if content is not None:
        status = content[0]
        process = content[1]
        if status == "wait_in":
            delete_status_by_user_date(account_id, current_date)

    if process is not None:
        return reminder_message("sign_in_done")

    return sign_in_message()


@tornado.gen.coroutine
def sign_in(account_id, current_date, _, __):
    content = yield sign_in_content(account_id, current_date)

    yield push_message(account_id, content)
