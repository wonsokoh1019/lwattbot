#!/bin/env python
# -*- coding: utf-8 -*-
"""
internal hello
"""
import logging
import tornado.web
import time
import uuid
import asyncio
from calender.externals.sendMessage import push_message
from calender.common import globalData
from calender.externals.richmenu import *
from calender.externals.calenderReq import *
from calender.constant import API_BO, RICH_MENUS, RECEIVE_ACCOUNT, LOCAL
from calender.model.data import *
from calender.common import globalData
from calender.message import *
from calender.checkParameter import *
from calender.model.processStatusDBHandle import *
from calender.model.calenderDBHandle import *

LOGGER = logging.getLogger("calender")


@tornado.gen.coroutine
def deal_logic(checker):
    LOGGER.info("begin deal check_para")
    request = {}

    if checker.account_id is not None:
        request["accountId"] = checker.account_id
    elif checker.room_id is not None:
        request["roomId"] = checker.room_id

    create_time = time.time()
    current_date = time.strftime("%Y-%m-%d", time.localtime(create_time))
    account_id = checker.account_id
    room_id = checker.room_id

    if checker.cmd == UserCmd.MESSAGE:
        LOGGER.info("begin to deal room_id:%s account_id:%s",
                    str(room_id), str(account_id))
        contents = yield deal_message(account_id, checker.text, create_time)

        if contents is None:
            return True, "contents is None"

        for content in contents:
            request["content"] = content
            error_code = yield push_message(request)
            if error_code:
                LOGGER.info("yield deal_message failed. room_id:%s "
                            "account_id:%s",
                            str(room_id), str(account_id))
                return False, "yield error_message failed."

        return True, None

    elif checker.cmd == UserCmd.START:
        request["content"] = first_message()
        error_code = yield push_message(request)
        if error_code:
            LOGGER.info("yield first_message failed. room_id:%s account_id:%s",
                        str(room_id), str(account_id))
            return False, "send message failed."

        request["content"] = image_introduce()
        error_code = yield push_message(request)
        if error_code:
            LOGGER.info("image_interduce failed. room_id:%s account_id:%s",
                        str(room_id), str(account_id))
            return False, "send message failed."
        error_code, error_message = yield sign(account_id)
        return error_code, error_message

    elif checker.cmd == UserCmd.CLEAN:
        clean_status_by_user(account_id, current_date)
        clean_schedule_by_user(account_id, current_date)
        return True, None

    elif checker.cmd == UserCmd.TO_FIRST:
        request["content"] = to_first()
        error_code = yield push_message(request)
        if error_code:
            LOGGER.info("yield to_first failed. room_id:%s account_id:%s",
                        str(room_id), str(account_id))
            return False, "send message failed."
        return True, None
    elif checker.cmd == UserCmd.SIGN_IN:
        request["content"] = yield sign_in(account_id, create_time)
        error_code = yield push_message(request)
        if error_code:
            LOGGER.info("yield sgin in failed. room_id:%s account_id:%s",
                        str(room_id), str(account_id))
            return False, "send message failed."
        return True, None

    elif checker.cmd == UserCmd.SIGN_OUT:
        request["content"] = yield sign_out(account_id, create_time)
        error_code = yield push_message(request)
        if error_code:
            LOGGER.info("sign_out failed. room_id:%s account_id:%s",
                        str(room_id), str(account_id))
            return False, "send message failed."
        return True, None

    elif checker.cmd == UserCmd.DIRECT_SIGN_IN:
        request["content"] = yield deal_sign_in(account_id,
                                                create_time, create_time)
        error_code = yield push_message(request)
        if error_code:
            LOGGER.info("yield direct sgin in failed. "
                        "room_id:%s account_id:%s",
                        str(room_id), str(account_id))
            return False, "send message failed."
        return True, None

    elif checker.cmd == UserCmd.DIRECT_SIGN_OUT:
        request["content"] = yield deal_sign_out(account_id, create_time,
                                                 create_time)
        error_code = yield push_message(request)
        if error_code:
            LOGGER.info("yield direct sgin out failed. "
                        "room_id:%s account_id:%s",
                        str(room_id), str(account_id))
            return False, "send message failed."
        return True, None

    elif checker.cmd == UserCmd.MANUAL_SIGN_IN:
        contents = yield manual_sign_in(account_id, create_time)
        if contents is None:
            LOGGER.info("yield manual_sign_in failed. "
                        "room_id:%s account_id:%s",
                        str(room_id), str(account_id))
            return False, "manual_sign_in failed."
        for content in contents:
            request["content"] = content
            error_code = yield push_message(request)
            if error_code:
                LOGGER.info("yield manual_sign_in failed. "
                            "room_id:%s account_id:%s",
                            str(room_id), str(account_id))
                return False, "send message failed."
        return True, None

    elif checker.cmd == UserCmd.MANUAL_SIGN_OUT:
        contents = yield manual_sign_out(account_id, create_time)
        if contents is None:
            LOGGER.info("yield manual_sign_out failed. "
                        "room_id:%s account_id:%s",
                        str(room_id), str(account_id))
            return False, "manual_sign_out failed."
        for content in contents:
            request["content"] = content
            error_code = yield push_message(request)
            if error_code:
                LOGGER.info("yield manual_sign_out failed. "
                            "room_id:%s account_id:%s",
                            str(room_id), str(account_id))
                return False, "send message failed."
        return True, None

    elif checker.cmd == UserCmd.CONFIRM_IN:
        message = checker.post_back
        if checker.post_back is None:
            message = checker.text

        content = yield confirm_in(account_id, message)
        if content is not None:
            request["content"] = content
            error_code = yield push_message(request)
            if error_code:
                LOGGER.info("yield confirm in failed. "
                            "room_id:%s account_id:%s",
                            str(room_id), str(account_id))
                return False, "send message failed."
            insert_replace_status_by_user_date(account_id, current_date,
                                    status="in_done", process="sign_in_done")
            return True, None
        return False, "confirm in failed."

    elif checker.cmd == UserCmd.CONFIRM_OUT:
        message = checker.post_back
        if checker.post_back is None:
            message = checker.text

        contents, success = yield confirm_out(account_id, message)
        if contents is None:
            return False, "confirm out failed."
        for content in contents:
            request["content"] = content
            error_code = yield push_message(request)
            if error_code:
                LOGGER.info("yield confirm_out failed. "
                            "room_id:%s account_id:%s",
                            str(room_id), str(account_id))
                return False, "send message failed."
        if success:
            set_status_by_user_date(account_id, current_date,
                                    status="out_done", process="sign_out_done")
        return True, None


@tornado.gen.coroutine
def sign(account_id):
    if account_id is None:
        LOGGER.error("account_id is None.")
        return False
    rich_menu_id = globalData.get_value(RICH_MENUS[LOCAL]["name"], None)
    if rich_menu_id is None:
        LOGGER.error("get rich_menu_id failed.")
        return False, "get rich_menu_id failed."

    return set_user_specific_rich_menu(rich_menu_id, account_id)


@tornado.gen.coroutine
def sign_in(account_id, create_time):

    local_time = time.localtime(create_time)
    current_date = time.strftime("%Y-%m-%d", local_time)
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
def sign_out(account_id, create_time):
    local_time = time.localtime(create_time)
    current_date = time.strftime("%Y-%m-%d", local_time)
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
def deal_sign_in(account_id, create_time, sign_time, manual_flag=False):
    local_time = time.localtime(create_time)
    current_date = time.strftime("%Y-%m-%d", local_time)
    content = get_status_by_user(account_id, current_date)

    if content is not None:
        status = content[0]
        process = content[1]
        if status == "in_done" or process is not None:
            return invalid_message()

    return deal_sign_in_message(sign_time, manual_flag)


@tornado.gen.coroutine
def deal_sign_out(account_id, create_time, sign_time, manual_flag=False):
    local_time = time.localtime(create_time)
    current_date = time.strftime("%Y-%m-%d", local_time)
    content = get_status_by_user(account_id, current_date)

    process = None
    if content is not None:
        status = content[0]
        process = content[1]
        if status == "out_done":
            return invalid_message()

    if process is None or process != "sign_in_done":
        return invalid_message()

    return deal_sign_out_message(sign_time, manual_flag)


@tornado.gen.coroutine
def manual_sign_in(account_id, create_time):
    yield asyncio.sleep(1)

    local_time = time.localtime(create_time)
    current_date = time.strftime("%Y-%m-%d", local_time)
    content = get_status_by_user(account_id, current_date)

    if content is not None and content[1] is not None:
        return [invalid_message()]

    insert_replace_status_by_user_date(account_id, current_date, "wait_in")

    return manual_sign_in_message()


@tornado.gen.coroutine
def manual_sign_out(account_id, create_time):
    yield asyncio.sleep(1)

    local_time = time.localtime(create_time)
    current_date = time.strftime("%Y-%m-%d", local_time)
    content = get_status_by_user(account_id, current_date)

    if content is None or content[1] is None or content[1] != "sign_in_done":
        return [invalid_message()]

    set_status_by_user_date(account_id, current_date, "wait_out")

    return manual_sign_out_message()


@tornado.gen.coroutine
def send_to_admin(content):
    request = {}
    request["accountId"] = RECEIVE_ACCOUNT
    request["content"] = content
    error_code = yield push_message(request)
    if error_code:
        LOGGER.info("yield send to admin failed. account_id:%s",
                    RECEIVE_ACCOUNT)
        return False, "send message failed."
    return error_code, None


@tornado.gen.coroutine
def confirm_in(account_id, callback):
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
def confirm_out(account_id, callback):
    pos = callback.find("time=")
    str_time = callback[pos+5:]
    my_time = int(str_time)

    local_time = time.localtime(my_time)

    current_date = time.strftime("%Y-%m-%d", local_time)
    # local_time_s = time.strftime("%Y-%m-%d %H:%M:%S",
    #                              time.localtime(my_time))
    """
    current_date = time.strftime("%Y-%m-%d", local_time)

    calender_id = globalData.get_value(API_BO["calendar"]["name"])
    if calender_id is None:
        calender_id = get_calender_id()
        if calender_id is None:
            LOGGER.info("calender_id is None account_id:%s, "
                        "room_id:%s", str(account_id))
            return False, "calender_id is None."
    """

    info = get_schedule_by_user(account_id, current_date)
    if info is None:
        return None, False
    schedule_id = info[0]
    begin_time = info[1]
    """
        if not modify_schedules(calendar_id, begin_time, my_time, my_time):
            LOGGER.info("modify_schedules failed account_id:%s",
                        str(account_id))
        if schedule_id is None:
            LOGGER.info("schedule_id is None account_id:%s",
                        str(account_id))
            return None, False
        modify_schedule_by_user(schedule_id, my_time)
    else:
        LOGGER.info("schedules has exist. account_id:%s, room_id:%s",
                    str(account_id))
        return None, False
    """
    modify_schedule_by_user(schedule_id, my_time)
    LOGGER.info("schedule_id is None account_id:%s", str(account_id))

    if my_time < begin_time:
        yield asyncio.sleep(1)
        set_status_by_user_date(account_id, current_date, status="wait_out")
        return number_message(), False

    hours = int((my_time - begin_time)/3600)
    min = int(((my_time - begin_time) % 3600)/60)
    # text = confirm_out_send_to_admin_message(account_id,
    #                                         local_time_s, hours, min)
    # yield send_to_admin(text)

    return [confirm_out_message(my_time, hours, min)], True


@tornado.gen.coroutine
def deal_message(account_id, message, create_time):

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
                                     create_time, user_time_ticket, True)
        set_status_by_user_date(account_id, current_date, status="in_done")
        return [content]
    if status == "wait_out":
        content = yield deal_sign_out(account_id,
                                      create_time, user_time_ticket, True)
        set_status_by_user_date(account_id, current_date, status="out_done")
        return [content]
    if process == "sign_in_done" or process == "sign_out_done":
        return [invalid_message()]

    LOGGER.info("can't deal this message account_id:%s message:%s status:%s",
                account_id, message, status)
    return None


class CallbackHandler(tornado.web.RequestHandler):
    """
    /internal/hello
    """

    @tornado.gen.coroutine
    def post(self):
        """
        support post
        """

        path = self.request.uri
        LOGGER.info("request para path:%s", path)

        body = json.loads(self.request.body)
        checker = CheckParameter(body)
        if checker.cmd == UserCmd.DEFAULT:
            raise tornado.web.HTTPError(403, checker.error_message)

        LOGGER.info("request para body:%s", str(body))

        error_code, error_message = yield deal_logic(checker)
        if not error_code:
            raise tornado.web.HTTPError(403, error_message)
        self.finish()
