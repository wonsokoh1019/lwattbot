# !/bin/env python
# -*- coding: utf-8 -*-
import tornado.web
import logging
from calender.model.data import i18n_text, make_text
from calender.externals.send_message import push_message

LOGGER = logging.getLogger("calender")


def to_first_content():
    kr_text = i18n_text("ko_KR", "출근, 퇴근하실 때 하단 메뉴에서 "
                                 "각각에 맞는 ‘기록하기’ 버튼을 선택해 주세요")
    en_text = i18n_text("en_US", "Please select \"Record\" on the bottom of "
                                 "the menu each time when you clock in "
                                 "and clock out.")
    jp_text = i18n_text("ja_JP", "出勤、退勤するときに下のメニューから "
                                 "それぞれ「記録する」ボタンを選択してください。")

    i18n_texts = [kr_text, en_text, jp_text]

    text = make_text("출근, 퇴근하실 때 하단 메뉴에서 "
                     "각각에 맞는 ‘기록하기’ 버튼을 선택해 주세요", i18n_texts)
    return text


@tornado.gen.coroutine
def to_first(account_id, _, __, ___):
    content = to_first_content()
    yield push_message(account_id, content)
