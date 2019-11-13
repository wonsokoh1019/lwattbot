# !/bin/env python
# -*- coding: utf-8 -*-
import tornado.web
import logging
from calender.model.data import make_i18n_content_texts, make_button
from calender.externals.send_message import push_message
from calender.actions.message import reminder_message, create_button_actions
from calender.model.processStatusDBHandle import set_status_by_user_date, \
    get_status_by_user

LOGGER = logging.getLogger("calender")


def sign_out_message():
    jp_text = make_i18n_content_texts("ja_JP", "退勤時間の入力方式"
                                               "を選択してください。")
    en_text = make_i18n_content_texts("en_US", "Please select the clock-out "
                                               "time entry method.")
    kr_text = make_i18n_content_texts("ko_KR", "퇴근 시간 입력 "
                                               "방식을 선택해 주세요.")
    content_texts = [jp_text, en_text, kr_text]

    actions = create_button_actions("direct_sign_out", "manual_sign_out")

    return make_button("퇴근 시간 입력 방식을 선택해 주세요.",
                       actions, content_texts=content_texts)


@tornado.gen.coroutine
def sign_out_content(account_id, current_date):

    content = get_status_by_user(account_id, current_date)
    process = None
    if content is not None:
        status = content[0]
        process = content[1]
        if status == "wait_out":
            set_status_by_user_date(account_id, current_date, status="in_done")

    if process is None or process != "sign_in_done":
        return reminder_message(None)

    return sign_out_message()


@tornado.gen.coroutine
def sign_out(account_id, current_date, _, __):
    content = yield sign_out_content(account_id, current_date)

    yield push_message(account_id, content)
