# !/bin/env python
# -*- coding: utf-8 -*-
import time
import logging
from calender.model.data import make_i18n_label, make_message_action, \
    i18n_display_text, make_postback_action, \
    make_quick_reply_item, i18n_text, make_text
from calender.constant import API_BO, IMAGE_CAROUSEL, \
    RICH_MENUS, RECEIVE_ACCOUNT

LOGGER = logging.getLogger("calender")

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
