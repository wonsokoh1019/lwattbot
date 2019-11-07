#!/bin/env python
# -*- coding: utf-8 -*-
import tornado.web
import asyncio
import time
import uuid
import logging
from calender.model.data import *
from calender.externals.sendMessage import push_message
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
    current_date = time.strftime("%Y-%m-%d", time.localtime(my_time))
    # local_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(my_time))

    # calender_id = API_BO["calendar"]["test_calender_id"]
    info = get_schedule_by_user(account_id, current_date)
    schedule_id = str(uuid.uuid4()) + account_id
    if info is None:
        set_schedule_by_user(schedule_id, account_id, current_date,
                             my_time, my_end_time)
    """
    current_date = time.strftime("%Y-%m-%d", time.localtime(my_time))
    calender_id = globalData.get_value(API_BO["calendar"]["name"], None)
    if calender_id is None:
        calender_id = get_calender_id()
        if calender_id is None:
            LOGGER.info("calender_id is None account_id:%s, "
                "room_id:%s", str(account_id))
            return None
    my_end_time = my_time + 60
    info = get_schedule_by_user(account_id, date)
    if info is None:
        schedule_id = create_schedules(calendar_id,
                        my_time, my_end_time, my_time, account_id)
        if schedule_id is None:
            LOGGER.info("create_schedules failed account_id:%s, room_id:%s",
                            str(account_id))
            return None
        set_schedule_by_user(schedule_id, account_id, current_date,
                             my_time, my_end_time)
    else:
        LOGGER.info("schedules has exist."
                    "account_id:%s, room_id:%s", str(account_id))
        return None
    """
    # text = confirm_in_send_to_admin_message(account_id, local_time)
    # yield send_to_admin(text)

    return confirm_in_message()


@tornado.gen.coroutine
def confirm_in(account_id, current_date, callback):
    content = yield deal_confirm_in(account_id, callback)
    if content is None:
        return False, "confirm in failed. content is None"
    success_code, error_message = yield push_message(account_id, content)
    if success_code:
        insert_replace_status_by_user_date(account_id, current_date,
                                           status="in_done",
                                           process="sign_in_done")
    return success_code, error_message
