#!/bin/env python
# -*- coding: utf-8 -*-

import io
import logging
import json
from calender.model.data import make_size, make_bound, i18n_display_text, \
    make_i18n_label, make_postback_action, make_add_rich_menu, make_area
from calender.common import utils
from calender.constant import API_BO, OPEN_API, RICH_MENUS
import tornado.gen
from calender.common.utils import auth_get, auth_post, auth_del

LOGGER = logging.getLogger("calender")


def upload_content(file_path):
    headers = {
        "consumerKey": OPEN_API["consumerKey"],
        "x-works-apiid": OPEN_API["apiId"]
    }

    files = {'resourceName': open(file_path, 'rb')}

    url = API_BO["upload_url"]
    url = utils.replace_url_bot_no(url)

    LOGGER.info("upload content . url:%s", url)

    response = auth_post(url, files=files, headers=headers)
    if response.status_code != 200:
        LOGGER.info("push message failed. url:%s text:%s body:%s",
                    url, response.text, response.content)
        raise Exception("upload content. http return error.")
    if "x-works-resource-id" not in response.headers:
        LOGGER.error("invalid content. url:%s txt:%s headers:%s",
                    url, response.text, response.headers)
        raise Exception("upload content. not fond 'x-works-resource-id'.")
    return response.headers["x-works-resource-id"]


def make_add_rich_menu_body(rich_menu_name):
    size = make_size(2500, 1686)

    bound0 = make_bound(0, 0, 1250, 1286)
    jp_text0 = i18n_display_text("ja_JP", "出勤を記録する")
    en_text0 = i18n_display_text("en_US", "Record clock-in")
    kr_text0 = i18n_display_text("ko_KR", "출근 기록하기")
    display_text0 = [jp_text0, en_text0, kr_text0]

    jp_label_text0 = make_i18n_label("ja_JP", "出勤を記録する")
    en_label_text0 = make_i18n_label("en_US", "Record clock-in")
    kr_label_text0 = make_i18n_label("ko_KR", "출근 기록하기")
    display_label0 = [jp_label_text0, en_label_text0, kr_label_text0]

    action0 = make_postback_action("sign_in",
                                   display_text="출근 기록하기",
                                   label="출근 기록하기",
                                   i18n_display_texts=display_text0,
                                   i18n_labels=display_label0)

    bound1 = make_bound(1250, 0, 1250, 1286)
    jp_text1 = i18n_display_text("ja_JP", "退勤を記録する")
    en_text1 = i18n_display_text("en_US", "Record clock-out")
    kr_text1 = i18n_display_text("ko_KR", "퇴근 기록하기")
    display_text1 = [jp_text1, en_text1, kr_text1]

    jp_label_text1 = make_i18n_label("ja_JP", "退勤を記録する")
    en_label_text1 = make_i18n_label("en_US", "Record clock-out")
    kr_label_text1 = make_i18n_label("ko_KR", "퇴근 기록하기")
    display_label1 = [jp_label_text1, en_label_text1, kr_label_text1]

    action1 = make_postback_action("sign_out",
                                   display_text="퇴근 기록하기",
                                   label="퇴근 기록하기",
                                   i18n_display_texts=display_text1,
                                   i18n_labels=display_label1)

    bound2 = make_bound(0, 1286, 2500, 400)
    jp_text2 = i18n_display_text("ja_JP", "最初へ")
    en_text2 = i18n_display_text("en_US", "Start over")
    kr_text2 = i18n_display_text("ko_KR", "처음으로")
    display_text2 = [jp_text2, en_text2, kr_text2]

    jp_label_text2 = make_i18n_label("ja_JP", "最初へ")
    en_label_text2 = make_i18n_label("en_US", "Start over")
    kr_label_text2 = make_i18n_label("ko_KR", "처음으로")
    display_label2 = [jp_label_text2, en_label_text2, kr_label_text2]

    action2 = make_postback_action("to_first",
                                   display_text="처음으로",
                                   label="처음으로",
                                   i18n_display_texts=display_text2,
                                   i18n_labels=display_label2)

    rich_menu = make_add_rich_menu(
                    rich_menu_name,
                    size,
                    [
                        make_area(bound0, action0),
                        make_area(bound1, action1),
                        make_area(bound2, action2)
                    ])

    headers = API_BO["headers"]
    headers["consumerKey"] = OPEN_API["consumerKey"]

    url = API_BO["rich_menu_url"]
    url = utils.replace_url_bot_no(url)

    LOGGER.info("register richmenu. url:%s", url)

    response = auth_post(url, data=json.dumps(rich_menu), headers=headers)
    if response.status_code != 200:
        LOGGER.info("register richmenu failed. url:%s text:%s body:%s",
                    url, response.text, response.content)
        raise Exception("register richmenu. http return error.")

    LOGGER.info("register richmenu success. url:%s txt:%s body:%s",
                url, response.text, response.content)

    tmp = json.loads(response.content)
    return tmp["richMenuId"]


def set_rich_menu_image(resource_id, rich_menu_id):

    body = {"resourceId": resource_id}

    headers = API_BO["headers"]
    headers["consumerKey"] = OPEN_API["consumerKey"]

    url = API_BO["rich_menu_url"] + "/" + rich_menu_id + "/content"
    url = utils.replace_url_bot_no(url)
    LOGGER.info("set rich menu image . url:%s", url)

    response = auth_post(url, data=json.dumps(body), headers=headers)
    if response.status_code != 200:
        LOGGER.info("set rich menu image failed. url:%s text:%s body:%s",
                    url, response.text, response.content)
        raise Exception("set richmenu image. http return error.")

    LOGGER.info("set rich menu image success. url:%s txt:%s body:%s",
                url, response.text, response.content)


def set_user_specific_rich_menu(rich_menu_id, account_id):
    headers = API_BO["headers"]
    headers["consumerKey"] = OPEN_API["consumerKey"]
    url = API_BO["rich_menu_url"] + "/" \
          + rich_menu_id + "/account/" + account_id

    url = utils.replace_url_bot_no(url)

    response = auth_post(url, headers=headers)
    if response.status_code != 200:
        LOGGER.info("push message failed. url:%s text:%s body:%s",
                    url, response.text, response.content)
        raise Exception("set user specific richmenu. http return error.")
    LOGGER.info("set user specific richmenu success. url:%s txt:%s body:%s",
                url, response.text, response.content)


def get_rich_menus():
    headers = API_BO["headers"]
    headers["consumerKey"] = OPEN_API["consumerKey"]
    url = API_BO["rich_menu_url"]
    url = utils.replace_url_bot_no(url)

    LOGGER.info("push message begin. url:%s", url)
    response = auth_get(url, headers=headers)
    if response.status_code != 200:
        LOGGER.info("push message failed. url:%s text:%s body:%s",
                    url, response.text, response.content)
        return None

    LOGGER.info("push message success. url:%s txt:%s body:%s",
                url, response.text, response.content)

    tmp = json.loads(response.content)
    if "richmenus" in tmp:
        return tmp["richmenus"]

    return None


def canncel_user_specific_rich_menu(account_id):
    headers = API_BO["headers"]
    headers["consumerKey"] = OPEN_API["consumerKey"]
    url = API_BO["rich_menu_url"] + "/account/" + account_id
    url = utils.replace_url_bot_no(url)

    response = auth_del(url, headers=headers)
    if response.status_code != 200:
        LOGGER.info("push message failed. url:%s text:%s body:%s",
                    url, response.text, response.content)
        raise Exception("canncel user specific richmenu. http return error.")
    LOGGER.info("push message success. url:%s txt:%s body:%s",
                url, response.text, response.content)


def init_rich_menu(local=None):
    il8n_rich_menu_id = {}
    rich_menus = get_rich_menus()
    if rich_menus is not None:
        for menu in rich_menus:
            if local is not None and local in RICH_MENUS:
                if str(menu["name"]) == RICH_MENUS[local]["name"]:
                    il8n_rich_menu_id[RICH_MENUS[local]["name"]] = \
                        menu["richMenuId"]
                    break
            for tmp_local, info in RICH_MENUS.items():
                if str(menu["name"]) == info["name"]:
                    il8n_rich_menu_id[info["name"]] = menu["richMenuId"]
                    return il8n_rich_menu_id

    if local in RICH_MENUS and \
            RICH_MENUS[local]["name"] not in il8n_rich_menu_id:

        rich_menu_id = make_add_rich_menu_body(RICH_MENUS[local]["name"])

        resource_id = upload_content(RICH_MENUS[local]["path"])
        set_rich_menu_image(resource_id, rich_menu_id)

        il8n_rich_menu_id[RICH_MENUS[local]["name"]] = rich_menu_id
        return il8n_rich_menu_id

    for local, info in RICH_MENUS.items():
        if info["name"] not in il8n_rich_menu_id:
            rich_menu_id = make_add_rich_menu_body(info["name"])

            resource_id = upload_content(info["path"])
            set_rich_menu_image(resource_id, rich_menu_id)
            il8n_rich_menu_id[info["name"]] = rich_menu_id

    return il8n_rich_menu_id
