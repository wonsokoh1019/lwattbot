# !/bin/env python
# -*- coding: utf-8 -*-
import tornado.web
import logging
from calender.model.data import i18n_text, make_text, make_quick_reply
from calender.externals.send_message import push_message
from calender.actions.message import invalid_message, TimeStruct, \
    create_quick_replay_items
from calender.model.processStatusDBHandle import get_status_by_user

LOGGER = logging.getLogger("calender")


def deal_sign_in_message(sign_time, manual_flag):
    call_back = "sign_in"
    if manual_flag:
        call_back = "manual_sign_in"

    my_time = TimeStruct(sign_time)

    jp_text = i18n_text("ja_JP", "現在時間 " + my_time.month + "月 "
                        + my_time.date + "日 "
                        + my_time.week_date_jp + " "
                        + my_time.interval_jp + " "
                        + my_time.hours + "時 " +
                        my_time.min + "分で出勤時間を登録しますか？")
    en_text = i18n_text("en_US", "Register the current time "
                        + my_time.month + ", "
                        + my_time.date + " "
                        + my_time.week_date_en + " at "
                        + my_time.hours + ":"
                        + my_time.min + " "
                        + my_time.interval_en + " as clock-out time?")
    kr_text = i18n_text("ko_KR", "현재 시간 " + my_time.month + "월 "
                        + my_time.date + "일 "
                        + my_time.week_date_kr + " "
                        + my_time.interval_kr + " "
                        + my_time.hours + "시 "
                        + my_time.min + "분으로 출근 시간 등록하시겠습니까?")

    text = make_text("현재 시간 " + my_time.month + "월 "
                     + my_time.date + "일 "
                     + my_time.week_date_kr + " "
                     + my_time.interval_kr + " "
                     + my_time.hours + "시 "
                     + my_time. min + "분으로 출근 시간 등록하시겠습니까?",
                     [jp_text, en_text, kr_text])

    if manual_flag:
        jp_text = i18n_text("ja_JP",
                            "入力した " + my_time.month + "月 "
                            + my_time.date + "日 "
                            + my_time.week_date_jp + " "
                            + my_time.interval_jp + " "
                            + my_time.hours + "時 "
                            + my_time.min + "分で出勤時間を登録しますか？")
        en_text = i18n_text("en_US",
                            "Register the entered " + my_time.month + ", "
                            + my_time.date + " "
                            + my_time.week_date_en + " at "
                            + my_time.hours + ":"
                            + my_time.min + " "
                            + my_time.interval_en + " as clock-out time?")
        kr_text = i18n_text("ko_KR",
                            "입력하신 " + my_time.month + "월 "
                            + my_time.date + "일 "
                            + my_time.week_date_kr + " "
                            + my_time.interval_kr + " "
                            + my_time.hours + "시 "
                            + my_time.min
                            + "분으로 출근 시간을 등록하시겠습니까?")

        text = make_text(
            "입력하신 " + my_time.month + "월 "
            + my_time.date + "일 "
            + my_time.week_date_kr + " "
            + my_time.interval_kr + " "
            + my_time.hours + "시 "
            + my_time.min + "분으로 출근 시간을 등록하시겠습니까?",
            [jp_text, en_text, kr_text])

    content = text

    reply_items = create_quick_replay_items(
        "confirm_in&time=" + my_time.str_current_time_tick, call_back)

    content["quickReply"] = make_quick_reply(reply_items)

    return content


@tornado.gen.coroutine
def deal_sign_in(account_id, current_date, sign_time, manual_flag=False):
    content = get_status_by_user(account_id, current_date)

    if content is not None:
        status = content[0]
        process = content[1]
        if status == "in_done" or process is not None:
            return invalid_message()

    return deal_sign_in_message(sign_time, manual_flag)


@tornado.gen.coroutine
def direct_sign_in(account_id, current_date, sign_time, _):
    content = yield deal_sign_in(account_id, current_date, sign_time)
    if content is None:
        return False, "direct sign in. content is None"
    success_code, error_message = yield push_message(account_id, content)
    return success_code, error_message
