#!/bin/env python
# -*- coding: utf-8 -*-
import tornado.web
import time
import logging
from calender.model.data import *
from calender.externals.sendMessage import push_messages
from calender.actions.message import invalid_message, error_message
from calender.actions.direct_sign_in import deal_sign_in
from calender.actions.direct_sign_out import deal_sign_out
from calender.model.processStatusDBHandle import get_status_by_user, \
    set_status_by_user_date

LOGGER = logging.getLogger("calender")


@tornado.gen.coroutine
def deal_user_message(account_id, message, create_time):

    local_time = time.localtime(create_time)
    current_date = time.strftime("%Y-%m-%d", local_time)
    content = get_status_by_user(account_id, current_date)

    if content is None or content[0] is None:
        LOGGER.info("status is None account_id:%s message:%s content:%s",
                    account_id, message, str(content))
        return None

    status = content[0]
    process = content[1]
    try:
        user_time = int(message)
    except Exception as e:
        if status == "wait_in" or status == "wait_out":
            return error_message()
        else:
            return None

    tm = (local_time.tm_year, local_time.tm_mon, local_time.tm_mday,
          int(user_time/100), int(user_time % 100), 00, local_time.tm_wday,
          local_time.tm_yday, local_time.tm_isdst)

    user_time_ticket = int(time.mktime(tm))

    if (status == "wait_in" or status == "wait_out") \
            and (user_time < 0 or user_time > 2400):
        return error_message()

    if status == "wait_in":
        content = yield deal_sign_in(account_id,
                                     current_date, user_time_ticket, True)
        set_status_by_user_date(account_id, current_date, status="in_done")
        return [content]
    if status == "wait_out":
        content = yield deal_sign_out(account_id,
                                      current_date, user_time_ticket, True)
        set_status_by_user_date(account_id, current_date, status="out_done")
        return [content]
    if process == "sign_in_done" or process == "sign_out_done":
        return [invalid_message()]

    LOGGER.info("can't deal this message account_id:%s message:%s status:%s",
                account_id, message, status)
    return None


@tornado.gen.coroutine
def deal_message(account_id, message, create_time):
    contents = yield deal_user_message(account_id, message, create_time)
    if contents is None:
        return False, "confirm out failed."

    success_code, error_message = yield push_messages(account_id, contents)
    return success_code, error_message
