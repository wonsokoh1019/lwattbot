# !/bin/env python
# -*- coding: utf-8 -*-
import tornado.web
import logging
from calender.model.data import i18n_text, make_text, make_i18n_image_url, \
    make_i18n_label, i18n_display_text, \
    make_postback_action, make_image_carousel_column, make_image_carousel
from calender.constant import RICH_MENUS, LOCAL, IMAGE_CAROUSEL
from calender.externals.send_message import push_messages
from calender.common.global_data import get_value
from calender.externals.richmenu import set_user_specific_rich_menu

LOGGER = logging.getLogger("calender")

def first_message():
    kr_text = i18n_text("ko_KR", "안녕하세요, 출퇴근 시간을 입력하고 "
                                 "관리할 수 있도록 도와드리는 "
                                 "LINE WORKS의 근태관리 봇 입니다.")
    en_text = i18n_text("en_US", "Hello, I'm an attendance management "
                                 "bot of LINE WORKS that helps your "
                                 "timeclock management and entry.")
    jp_text = i18n_text("ja_JP", "こんにちは。出退勤の時間を入力して "
                                 "管理できるようサポートするLINE WORKSの "
                                 "勤怠管理Botです。")

    i18n_texts = [kr_text, en_text, jp_text]

    text = make_text("안녕하세요, 출퇴근 시간을 입력하고 "
                     "관리할 수 있도록 도와드리는 "
                     "LINE WORKS의 근태관리 봇 입니다.",
                     i18n_texts)
    return text


def image_introduce():
    resource_kr0 = make_i18n_image_url("ko_KR",
                                       IMAGE_CAROUSEL["resource_url"]["kr"][0])
    resource_en0 = make_i18n_image_url("en_US",
                                       IMAGE_CAROUSEL["resource_url"]["en"][0])
    resource_jp0 = make_i18n_image_url("ja_JP",
                                       IMAGE_CAROUSEL["resource_url"]["jp"][0])
    i18n_resource0 = [resource_kr0, resource_en0, resource_jp0]

    jp_text0 = make_i18n_label("ja_JP", "今使ってみてください")
    en_text0 = make_i18n_label("en_US", "Try it now")
    kr_text0 = make_i18n_label("ko_KR", "지금 사용해 보세요")
    display_label0 = [jp_text0, en_text0, kr_text0]

    display_text_jp0 = i18n_display_text("ja_JP",
                                         "ボタンをクリックするだけで簡単に出"
                                         "退勤時間を記録することができます。")
    display_text_en0 = i18n_display_text("en_US",
                                         "Timeclock can be recorded "
                                         "easily just by clicking buttons")
    display_text_kr0 = i18n_display_text("ko_KR",
                                         "버튼 클릭만으로 손쉽게 "
                                         "출퇴근  시간을 기록할 수 있습니다")
    i18n_display_text0 = [display_text_jp0, display_text_en0, display_text_kr0]
    action1 = make_postback_action("a",
                                   display_text="버튼 클릭만으로 손쉽게 출퇴근 "
                                                "시간을 기록할 수 있습니다",
                                   i18n_display_texts=i18n_display_text0,
                                   label="지금 사용해 보세요",
                                   i18n_labels=display_label0)

    column1 = make_image_carousel_column(
        image_url=IMAGE_CAROUSEL["resource_url"]["kr"][0],
        i18n_image_urls=i18n_resource0,
        action=action1)

    resource_kr1 = make_i18n_image_url("ko_KR",
                                       IMAGE_CAROUSEL["resource_url"]["kr"][1])
    resource_en1 = make_i18n_image_url("en_US",
                                       IMAGE_CAROUSEL["resource_url"]["en"][1])
    resource_jp1 = make_i18n_image_url("ja_JP",
                                       IMAGE_CAROUSEL["resource_url"]["jp"][1])
    i18n_resource1 = [resource_kr1, resource_en1, resource_jp1]

    display_text_jp1 = \
        i18n_display_text("ja_JP",
                          "入力された勤怠記録は、"
                          "共有カレンダー に自動で入力されます。")
    display_text_en1 = \
        i18n_display_text("en_US",
                          "Entered attendance records are automatically "
                          "entered in Shared Calendar")
    display_text_kr1 = \
        i18n_display_text("ko_KR",
                          "입력된 근태 기록은 공유 "
                          "캘린더에 자동으로 입력됩니다")
    i18n_display_text1 = [display_text_jp1, display_text_en1, display_text_kr1]

    action2 = \
        make_postback_action("b",
                             display_text="입력된 근태 기록은 공유 "
                                          "캘린더에 자동으로 입력됩니다",
                             i18n_display_texts=i18n_display_text1,
                             label="지금 사용해 보세요",
                             i18n_labels=display_label0)
    column2 = \
        make_image_carousel_column(
            image_url=IMAGE_CAROUSEL["resource_url"]["kr"][1],
            i18n_image_urls=i18n_resource1,
            action=action2)

    resource_kr2 = make_i18n_image_url("ko_KR",
                                       IMAGE_CAROUSEL["resource_url"]["kr"][2])
    resource_en2 = make_i18n_image_url("en_US",
                                       IMAGE_CAROUSEL["resource_url"]["en"][2])
    resource_jp2 = make_i18n_image_url("ja_JP",
                                       IMAGE_CAROUSEL["resource_url"]["jp"][2])
    i18n_resource2 = [resource_kr2, resource_en2, resource_jp2]

    display_text_jp2 = i18n_display_text("ja_JP",
                                         "勤怠管理共有カレンダーですべての"
                                         "社員の勤怠記録を一目で確認できます。")
    display_text_en2 = i18n_display_text("en_US",
                                         "Attendance records of all employees "
                                         "can be checked at a glance via "
                                         "Attendance Management "
                                         "Shared Calendar")
    display_text_kr2 = i18n_display_text("ko_KR",
                                         "공유 캘린더에서 모든 직원의 근태 "
                                         "기록을 한눈에 확인해볼 수 있습니다")
    i18n_display_text2 = [display_text_jp2, display_text_en2, display_text_kr2]

    action3 = make_postback_action("c",
                                   display_text="공유 캘린더에서 모든 직원의 "
                                                "근태 기록을 한눈에 확인해볼 "
                                                "수 있습니다",
                                   i18n_display_texts=i18n_display_text2,
                                   label="지금 사용해 보세요",
                                   i18n_labels=display_label0)

    column3 = \
        make_image_carousel_column(
            image_url=IMAGE_CAROUSEL["resource_url"]["kr"][2],
            i18n_image_urls=i18n_resource2,
            action=action3)

    columns = [column1, column2, column3]
    return make_image_carousel(columns)


@tornado.gen.coroutine
def sign(account_id):
    if account_id is None:
        LOGGER.error("account_id is None.")
        return False
    rich_menu_id = get_value(RICH_MENUS[LOCAL]["name"], None)
    if rich_menu_id is None:
        LOGGER.error("get rich_menu_id failed.")
        return False, "get rich_menu_id failed."

    return set_user_specific_rich_menu(rich_menu_id, account_id)


@tornado.gen.coroutine
def start_content(account_id):
    success_code, error_message = yield sign(account_id)
    if not success_code:
        raise tornado.web.HTTPError(500, error_message)
    content1 = first_message()
    content2 = image_introduce()
    return [content1, content2]


@tornado.gen.coroutine
def start(account_id, _, __, ___):
    contents = yield start_content(account_id)
    success_code, error_message = yield push_messages(account_id, contents)
    return success_code, error_message
