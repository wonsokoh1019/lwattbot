#!/bin/env python
# -*- coding: utf-8 -*-
import tornado.gen
import asyncio
import time
import uuid
import logging
from datetime import datetime
from tornado.web import HTTPError
from calender.common import global_data
from calender.common.local_timezone import local_date_time
from calender.model.data import i18n_text, make_text
from calender.externals.send_message import push_message
from calender.actions.message import invalid_message, prompt_input
from calender.model.processStatusDBHandle import get_status_by_user, \
    insert_replace_status_by_user_date
from calender.model.calenderDBHandle import set_schedule_by_user, \
    get_schedule_by_user

LOGGER = logging.getLogger("calender")


def confirm_in_message():
    jp_text = i18n_text("ja_JP", "出勤時間の登録が完了しました。")
    en_text = i18n_text("en_US", "Clock-in time has been registered.")
    kr_text = i18n_text("ko_KR", "출근 시간 등록이 완료되었습니다.")

    text = make_text("출근 시간 등록이 완료되었습니다.",
                     [jp_text, en_text, kr_text])
    return text


@tornado.gen.coroutine
def deal_confirm_in(account_id, callback):
    pos = callback.find("time=")
    str_time = callback[pos+5:]
    my_time = int(str_time)
    my_end_time = my_time + 60
    date_time = local_date_time(my_time)
    current_date = datetime.strftime(date_time, '%Y-%m-%d')

    info = get_schedule_by_user(account_id, current_date)
    schedule_id = str(uuid.uuid4()) + account_id
    if info is not None:
        raise HTTPError(500, "Internal data error")
    # todo deal calender api logic
    set_schedule_by_user(schedule_id, account_id, current_date,
                         my_time, my_end_time)
    return confirm_in_message()


@tornado.gen.coroutine
def confirm_in(account_id, current_date, _, callback):
    content = yield deal_confirm_in(account_id, callback)
    yield push_message(account_id, content)

    insert_replace_status_by_user_date(account_id, current_date,
                                       status="in_done",
                                       process="sign_in_done")
