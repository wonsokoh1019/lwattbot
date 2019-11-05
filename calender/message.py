# !/bin/env python
# -*- coding: utf-8 -*-
import time
from calender.model.data import *
from calender.constant import API_BO, IMAGE_CAROUSEL, \
    RICH_MENUS, RECEIVE_ACCOUNT


en_week = ["Monday", "Tuesday", "Wednesday", "Thursday",
           "Friday", "Saturday", "Sunday"]
kr_week = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
jp_week = ["月曜日", "火曜日", "水曜日", "木曜日", "金曜日", "土曜日", "日曜日"]

en_month = ["January", "February", "March", "April", "May", "June", "July",
            "August", "September", "October", "November", "December"]
# kr_month = ["일월","이월","삼월","사월","오월","유월","칠월","팔월",
# "구월","시월","십이월","십이월"]
# jp_month = ["いちがつ", "にがつ", "さんがつ", "しがつ", "ごがつ", "ろくがつ",
# "しちがつ", "はちがつ", "くがつ", "じゅうがつ", "じゅういちがつ", "じゅうにがつ"]


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


def to_first():
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


def create_button_actions(direct_sign_callback, manual_sign_callback):
    jp_text1 = make_i18n_label("ja_JP", "現在の時刻")
    en_text1 = make_i18n_label("en_US", "Current time")
    kr_text1 = make_i18n_label("ko_KR", "현재 시간")
    display_label1 = [jp_text1, en_text1, kr_text1]
    action1 = make_message_action("현재 시간", direct_sign_callback,
                                  i18n_labels=display_label1)

    jp_text2 = make_i18n_label("ja_JP", "直接入力")
    en_text2 = make_i18n_label("en_US", "Manually enter")
    kr_text2 = make_i18n_label("ko_KR", "직접 입력")
    display_label2 = [jp_text2, en_text2, kr_text2]
    action2 = make_message_action("직접 입력", manual_sign_callback,
                                  i18n_labels=display_label2)

    return [action1, action2]


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


def create_quick_replay_items(confirm_callback, previous_callback):
    jp_text = make_i18n_label("ja_JP", "はい")
    en_text = make_i18n_label("en_US", "yes")
    kr_text = make_i18n_label("ko_KR", "예")
    display_label = [jp_text, en_text, kr_text]

    display_text_jp = i18n_display_text("ja_JP", "はい")
    display_text_en = i18n_display_text("en_US", "yes")
    display_text_kr = i18n_display_text("ko_KR", "예")

    display_label_text = [display_text_jp, display_text_en, display_text_kr]

    action1 = make_postback_action(confirm_callback,
                                   label="예",
                                   i18n_labels=display_label,
                                   display_text="예",
                                   i18n_display_texts=display_label_text)
    reply_item1 = make_quick_reply_item(action1)

    jp_text2 = make_i18n_label("ja_JP", "いいえ")
    en_text2 = make_i18n_label("en_US", "No")
    kr_text2 = make_i18n_label("ko_KR", "아니요")
    display_label2 = [jp_text2, en_text2, kr_text2]

    display_text_jp2 = i18n_display_text("ja_JP", "いいえ")
    display_text_en2 = i18n_display_text("en_US", "No")
    display_text_kr2 = i18n_display_text("ko_KR", "아니요")
    display_label_text2 = [display_text_jp2,
                           display_text_en2,
                           display_text_kr2]
    action2 = make_postback_action(previous_callback,
                                   label="아니요",
                                   i18n_labels=display_label2,
                                   display_text="아니요",
                                   i18n_display_texts=display_label_text2)
    reply_item2 = make_quick_reply_item(action2)

    return [reply_item1, reply_item2]


class TimeStruct:
    def __init__(self, sign_time):
        local_time = time.localtime(sign_time)
        self.week_date_jp = jp_week[local_time.tm_wday]
        self.week_date_kr = kr_week[local_time.tm_wday]
        self.week_date_en = en_week[local_time.tm_wday]

        self.month = str(local_time.tm_mon)
        self.date = str(local_time.tm_mday)
        self.min = str(local_time.tm_min)

        self.interval_jp = "午前"
        self.interval_en = "AM"
        self.interval_kr = "오전"

        self.hours = str(local_time.tm_hour)
        if local_time.tm_hour > 12:
            self.interval_jp = "午後"
            self.interval_en = "PM"
            self.interval_kr = "오후"
            self.hours = str(local_time.tm_hour - 12)

        self.str_current_time_tick = str(sign_time)
        pos = self.str_current_time_tick.find(".")
        if pos != -1:
            self.str_current_time_tick = self.str_current_time_tick[:pos]


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


def deal_sign_out_message(sign_time, manual_flag=False):
    call_back = "sign_out"
    if manual_flag:
        call_back = "manual_sign_out"

    my_time = TimeStruct(sign_time)

    jp_text = i18n_text("ja_JP",
                        "現在時間 " + my_time.month + "月 "
                        + my_time.date + "日 "
                        + my_time.week_date_jp + " "
                        + my_time.interval_jp + " "
                        + my_time.hours + "時 "
                        + my_time.min + "分で退勤時間を登録しますか？")
    en_text = i18n_text("en_US",
                        "Register the current time "
                        + my_time.month + ", "
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
                        + my_time.min + "분으로 출근 시간을 등록하시겠습니까?")

    text = make_text(
        "입력하신 " + my_time.month + "월 "
        + my_time.date + "일 "
        + my_time.week_date_kr + " "
        + my_time.interval_kr + " "
        + my_time.hours + "시 "
        + my_time.min + "분으로 출근 시간을 등록하시겠습니까?",
        [jp_text, en_text, kr_text])

    if manual_flag:
        jp_text = i18n_text("ja_JP",
                            "入力した " + my_time.month + "月 "
                            + my_time.date + "日 "
                            + my_time.week_date_jp + " "
                            + my_time.interval_jp + " "
                            + my_time.hours + "時 "
                            + my_time.min + "分で退勤時間を登録しますか？")
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
                            + my_time.min + "분으로  퇴근 시간을 등록하시겠습니까?")

        text = make_text(
            "입력하신 " + my_time.month + "월 "
            + my_time.date + "일 "
            + my_time.week_date_kr + " "
            + my_time.interval_kr + " "
            + my_time.hours + "시 "
            + my_time.min + "분으로  퇴근 시간을 등록하시겠습니까?",
            [jp_text, en_text, kr_text])

    content = text

    reply_items = create_quick_replay_items(
        "confirm_out&time=" + my_time.str_current_time_tick, call_back)

    content["quickReply"] = make_quick_reply(reply_items)
    return content


def prompt_input():
    jp_text = i18n_text("ja_JP",
                        "時間を入力するときは、合計4桁の数字を時、"
                        "分の順番に入力してください。"
                        "例えば、午後8時20分を入力したい場合"
                        "は2020という数字を入力してください。")
    en_text = i18n_text("en_US",
                        "Please use the military time format "
                        "with a total of 4 numerical digits (hhmm) "
                        "when entering the time."
                        "For example, type 2020 to indicate 8:20 PM. ")
    kr_text = i18n_text("ko_KR",
                        "시간을 입력하실 때는 총 4자리 숫자를 시,"
                        "분 순서대로 기재해 주세요.예를 들어, "
                        "오후 8시 20분을 기재 하고 싶으시면 "
                        "2020이라는 숫자를 작성해 주시면 됩니다.")

    i18n_texts = [jp_text, en_text, kr_text]
    text = make_text(
        "시간을 입력하실 때는 총 4자리 숫자를 시,"
        "분 순서대로 기재해 주세요.예를 들어, "
        "오후 8시 20분을 기재 하고 싶으시면 "
        "2020이라는 숫자를 작성해 주시면 됩니다.",
        i18n_texts)
    return text


def number_message():
    jp_text = i18n_text("ja_JP",
                        "退勤時間を出勤時間よりも早い時間で作成されました。"
                        "もう一度退勤時間を確認して入力してください。")
    en_text = i18n_text("en_US",
                        "You have created your leave time "
                        "earlier than your leave time. "
                        "Please check your work time and enter again.")
    kr_text = i18n_text("ko_KR", "퇴근 시간을 출근 시간보다 "
                                 "이른 시간으로 작성하셨습니다. "
                                 "다시 한번 퇴근 시간을 확인하시고 입력해주세요. ")

    i18n_texts1 = [jp_text, en_text, kr_text]

    text1 = make_text("퇴근 시간을 출근 시간보다 이른 시간으로 작성하셨습니다. "
                      "다시 한번 퇴근 시간을 확인하시고 입력해주세요.",
                      i18n_texts1)

    text2 = prompt_input()
    return [text1, text2]


def error_message():
    jp_text = i18n_text("ja_JP", "申し訳ございません。"
                                 "作成した時間が理解できませんでした。"
                                 "もう一度時間入力の方法を確認し、"
                                 "時間を入力してください。")
    en_text = i18n_text("en_US", "Sorry, but unable to "
                                 "comprehend your composed time. "
                                 "Please check the time entry method again, "
                                 "and enter the time.")
    kr_text = i18n_text("ko_KR", "죄송합니다. 작성하신 시간을 "
                                 "이해하지 못하였습니다. "
                                 "다시 한 번 시간 입력 방법을 "
                                 "확인하시고 시간을 입력해 주세요.  ")

    i18n_texts1 = [jp_text, en_text, kr_text]

    text1 = make_text("죄송합니다. 작성하신 시간을 "
                      "이해하지 못하였습니다. "
                      "다시 한 번 시간 입력 방법을 "
                      "확인하시고 시간을 입력해 주세요. ",
                      i18n_texts1)

    text2 = prompt_input()
    return [text1, text2]


def invalid_message():

    jp_text = i18n_text("ja_JP", "テキストを理解していませんでした。"
                                 "出勤、退勤の際下のメニューからそれぞれに合った"
                                 "「記録する」ボタンを選択してください。")
    en_text = i18n_text("en_US", "I didn't understand the text. "
                                 "When you go to work or go home, "
                                 "Please select the appropriate "
                                 "\"Record\" button for each.")
    kr_text = i18n_text("ko_KR", "텍스트를 이해하지 못했습니다. "
                                 "출근, 퇴근하실 때 하단 메뉴에서 각각에 "
                                 "맞는 ‘기록하기’ 버튼을 선택해 주세요 .")

    i18n_texts1 = [jp_text, en_text, kr_text]
    text = make_text("텍스트를 이해하지 못했습니다. "
                     "출근, 퇴근하실 때 하단 메뉴에서 각각에 "
                     "맞는 ‘기록하기’ 버튼을 선택해 주세요 .", i18n_texts1)

    return text


def reminder_message(process):
    text = None
    if process == "sign_in_done":
        jp_text = i18n_text("ja_JP", "すでに登録済みの出勤時間があります。"
                                     "退勤するときに、下のメニューから"
                                     "「退勤を記録する」ボタンを選択してください。")
        en_text = i18n_text("en_US", "There is already a clock-in time. "
                                     "Please select \"Record\" on the "
                                     "bottom of the menu when you clock out.")
        kr_text = i18n_text("ko_KR", "이미 등록된 출근 시간이 있습니다. "
                                     "퇴근하실 때, 하단 메뉴에서  "
                                     "‘퇴근 기록하기’ 버튼을 선택해 주세요.")

        i18n_texts1 = [jp_text, en_text, kr_text]
        text = make_text("이미 등록된 출근 시간이 있습니다. "
                         "퇴근하실 때, 하단 메뉴에서  "
                         "‘퇴근 기록하기’ 버튼을 선택해 주세요.", i18n_texts1)

    elif process == "sign_out_done":
        jp_text = i18n_text("ja_JP", "すでに登録済みの退勤時間があります。"
                                     "出勤するときに、下のメニューから"
                                     "「出勤を記録する」ボタンを選択してください。")
        en_text = i18n_text("en_US", "There is already a clock-out time."
                                     "Please select \"Record\" on the bottom "
                                     "of the menu when you clock in.")
        kr_text = i18n_text("ko_KR", "이미 등록된 퇴근 시간이 있습니다."
                                     "출근하실 때, 하단 메뉴에서 "
                                     "‘출근 기록하기’ 버튼을 선택해 주세요.")

        i18n_texts1 = [jp_text, en_text, kr_text]
        text = make_text("이미 등록된 퇴근 시간이 있습니다."
                         "출근하실 때, 하단 메뉴에서 "
                         "‘출근 기록하기’ 버튼을 선택해 주세요.", i18n_texts1)
    elif process is None:
        jp_text = i18n_text("ja_JP", "今日の出勤時間が登録されていません。"
                                     "下のメニューから「出勤を記録する」"
                                     "ボタンを選択し、"
                                     "先に出勤時間を入力してください。")
        en_text = i18n_text("en_US", "Today's clock-in time "
                                     "has not been registered. "
                                     "Please select \"Record clock-in\" "
                                     "on the bottom of the menu, "
                                     "and enter your clock-in time.")
        kr_text = i18n_text("ko_KR", "오늘의 출근 시간이 등록되어 있지 않습니다. "
                                     "하단의 메뉴에서 ‘출근 기록하기’ "
                                     "버튼을 선택하여 출근 "
                                     "시간을 먼저 입력해 주세요.")

        i18n_texts1 = [jp_text, en_text, kr_text]
        text = make_text("오늘의 출근 시간이 등록되어 있지 않습니다. "
                         "하단의 메뉴에서 ‘출근 기록하기’ 버튼을 선택하여 "
                         "출근 시간을 먼저 입력해 주세요.",
                         i18n_texts1)
    return text


def manual_sign_in_message():
    jp_text = i18n_text("ja_JP", "出勤時間を直接入力してください。")
    en_text = i18n_text("en_US", "Please manually enter the clock-in time.")
    kr_text = i18n_text("ko_KR", "출근 시간을 직접 입력해 주세요. ")

    i18n_texts1 = [jp_text, en_text, kr_text]

    text1 = make_text("출근 시간을 직접 입력해 주세요. ", i18n_texts1)

    text2 = prompt_input()

    return [text1, text2]


def manual_sign_out_message():
    jp_text = i18n_text("ja_JP", "退勤時間を直接入力してください。")
    en_text = i18n_text("en_US", "Please manually enter the clock-out time.")
    kr_text = i18n_text("ko_KR", "퇴근 시간을 직접 입력해 주세요. ")

    i18n_texts1 = [jp_text, en_text, kr_text]

    text1 = make_text("퇴근 시간을 직접 입력해 주세요. ", i18n_texts1)

    text2 = prompt_input()

    return [text1, text2]


def confirm_in_send_to_admin_message(account_id, local_time):
    jp_text1 = i18n_text("ja_JP", account_id + " 出勤時間の登録:" + local_time)
    en_text1 = i18n_text("en_US", account_id + " Clock-in time:" + local_time)
    kr_text1 = i18n_text("ko_KR", account_id + " 출근 시간:" + local_time)
    text1 = make_text(account_id + " 출근 시간:" + local_time,
                      [jp_text1, en_text1, kr_text1])
    return text1


def confirm_in_message():
    jp_text = i18n_text("ja_JP", "出勤時間の登録が完了しました。")
    en_text = i18n_text("en_US", "Clock-in time has been registered.")
    kr_text = i18n_text("ko_KR", "출근 시간 등록이 완료되었습니다.")

    text = make_text("출근 시간 등록이 완료되었습니다.",
                     [jp_text, en_text, kr_text])
    return text


def confirm_out_send_to_admin_message(account_id, local_time, hours, min):
    jp_text1 = i18n_text("ja_JP",
                         account_id + " 退勤時間:"
                         + local_time + " 合計勤務時間は  "
                         + str(hours) + "時間 "
                         + str(min) + "分です。")
    en_text1 = i18n_text("en_US", account_id + " Clock-out time:"
                         + local_time + " total working hours for "
                         + str(hours) + " hours and "
                         + str(min) + " minutes.")
    kr_text1 = i18n_text("ko_KR",
                         account_id + " 퇴근 시간:"
                         + local_time + " 일 월요일 총 근무 시간은  "
                         + str(hours) + "시간 "
                         + str(min) + "분입니다.")
    text1 = make_text(
        account_id + " 퇴근 시간:" + local_time + " 일 월요일 총 근무 시간은  "
        + str(hours) + "시간 " + str(min) + "분입니다.",
        [jp_text1, en_text1, kr_text1])

    return text1


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
