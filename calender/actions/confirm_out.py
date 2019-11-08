#!/bin/env python
# -*- coding: utf-8 -*-
import tornado.gen
import asyncio
import time
import logging
from datetime import datetime
from tornado.web import HTTPError
from calender.common import global_data
from calender.common.local_timezone import local_date_time
from calender.model.data import i18n_text, make_text
from calender.externals.send_message import push_messages
from calender.actions.message import invalid_message, prompt_input, \
    en_month, TimeStruct, number_message
from calender.model.processStatusDBHandle import get_status_by_user, \
    set_status_by_user_date
from calender.model.calenderDBHandle import get_schedule_by_user, \
    modify_schedule_by_user

LOGGER = logging.getLogger("calender")


def confirm_out_message(my_time, hours, min):
    my_time = TimeStruct(my_time)

    jp_text = i18n_text("ja_JP", "退勤時間の登録が完了しました。"
                        + my_time.month + "月 "
                        + my_time.date + "日 "
                        + my_time.week_date_jp + "の合計勤務時間は  "
                        + str(hours) + "時間 "
                        + str(min) + "分です。")
    en_text = i18n_text("en_US",
                        "Clock-out time has been registered."
                        "The total working hours for "
                        + my_time.week_date_en + ", "
                        + en_month[int(my_time.month)] + " "
                        + my_time.date + " is "
                        + str(hours) + " hours and "
                        + str(min) + " minutes.")
    kr_text = i18n_text("ko_KR",
                        "퇴근 시간 등록이 완료되었습니다. "
                        + my_time.month + "월 "
                        + my_time.date + "일 "
                        + my_time.week_date_kr + " 총 근무 시간은 "
                        + str(hours) + "시간 "
                        + str(min) + "분입니다.")

    text = make_text(
        "퇴근 시간 등록이 완료되었습니다. "
        + my_time.month + "월 "
        + my_time.date + "일 "
        + my_time.week_date_kr + " 총 근무 시간은 "
        + str(hours) + "시간 "
        + str(min) + "분입니다.",
        [jp_text, en_text, kr_text])

    return text


@tornado.gen.coroutine
def deal_confirm_out(account_id, callback):
    pos = callback.find("time=")
    str_time = callback[pos+5:]
    my_time = int(str_time)

    date_time = local_date_time(my_time)
    current_date = datetime.strftime(date_time, '%Y-%m-%d')

    info = get_schedule_by_user(account_id, current_date)
    if info is None:
        raise HTTPError(500, "Internal data error")
    schedule_id = info[0]
    begin_time = info[1]

    # todo deal calender api logic
    modify_schedule_by_user(schedule_id, my_time)

    if my_time < begin_time:
        yield asyncio.sleep(1)
        set_status_by_user_date(account_id, current_date, status="wait_out")
        return number_message(), False

    hours = int((my_time - begin_time)/3600)
    min = int(((my_time - begin_time) % 3600)/60)

    return [confirm_out_message(my_time, hours, min)], True


@tornado.gen.coroutine
def confirm_out(account_id, current_date, _, callback):

    contents, success = yield deal_confirm_out(account_id, callback)

    yield push_messages(account_id, contents)

    if success:
        set_status_by_user_date(account_id, current_date,
                                status="out_done", process="sign_out_done")
