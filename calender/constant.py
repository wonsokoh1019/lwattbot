#!/bin/bash python3
# -*- coding: UTF-8 -*-
"""
constants.py Defining the constant used for a project.

"""
import os
from calender.constants.common import *
# ---------------------------------------------------------------------
# Constants and global variables
# ---------------------------------------------------------------------

SERVICE_CONSUMER_KEY = None
LOCAL = LANG
HEROKU_SERVER_ID = SERVER_ID
IP_TOKEN = TOKEN
PRIVATE_KEY_PATH = ABSDIR_OF_ROOT + "/key/" + PRIVATE_KEY_NAME

# SSL_KEY = ABSDIR_OF_ROOT + "/key/worksmobile_2019_key.pem"
# SSL_CERT = ABSDIR_OF_ROOT + "/key/worksmobile_2019_nginx_cert.pem"
RICH_MENUS = {
                "kr": {
                    "name": "calender_bot_rich_menu_kr",
                    "path": ABSDIR_OF_ROOT + "/image/kr/Rich_Menu.png"
                },
                "jp":
                {
                    "name": "calender_bot_rich_menu_jp",
                    "path": ABSDIR_OF_ROOT + "/image/jp/Rich_Menu.png"
                 },
                "en":
                {
                    "name": "calender_bot_rich_menu_en",
                    "path": ABSDIR_OF_ROOT + "/image/en/Rich_Menu.png"
                }
            }

IMAGE_CAROUSEL = {
                    "resource_url":
                    {
                        "kr": [LOCAL_ADDRESS + "static/kr/IMG_Carousel_01.png",
                               LOCAL_ADDRESS + "static/kr/IMG_Carousel_02.png",
                               LOCAL_ADDRESS + "static/kr/IMG_Carousel_03.png"],
                        "en": [LOCAL_ADDRESS + "static/en/IMG_Carousel_01.png",
                               LOCAL_ADDRESS + "static/en/IMG_Carousel_02.png",
                               LOCAL_ADDRESS + "static/en/IMG_Carousel_03.png"],
                        "jp": [LOCAL_ADDRESS + "static/jp/IMG_Carousel_01.png",
                               LOCAL_ADDRESS + "static/jp/IMG_Carousel_02.png",
                               LOCAL_ADDRESS + "static/jp/IMG_Carousel_03.png"]
                    }
                }
API_BO = {
            "headers": {
                "content-type": "application/json",
                "charset": "UTF-8"
            },
            "upload_url": "http://" + STORAGE_DOMAIN
                          + "/openapi/message/upload.api",
            "push_url": "https://" + DEVELOP_API_DOMAIN + "/r/"
                        + API_ID + "/message/v1/bot/_BOT_NO_/message/push",
            "rich_menu_url": "https://" + DEVELOP_API_DOMAIN + "/r/"
                             + API_ID + "/message/v1/bot/_BOT_NO_/richmenu",

            "calendar":
            {
                "name": "test_calendar",
                "test_calender_id": "test calender id",
                "create_calender_url": "https://" + DEVELOP_API_DOMAIN + "/"
                                       + API_ID + "/calendar/createCalendar",
                "get_calenders_url": "https://" + DEVELOP_API_DOMAIN + "/r/"
                                     + API_ID
                                     + "/calendar/rest/v1/users/me/"
                                       "calendarList",
                "create_schedule_url": "https://" + DEVELOP_API_DOMAIN + "/"
                                       + API_ID + "/calendar/createSchedule",
                "modify_schedule_url": "https://" + DEVELOP_API_DOMAIN + "/"
                                       + API_ID + "/calendar/modifySchedule",
                "TZone": "Asia/Seoul"
            },

            "TZone":
            {
                "external_key_url": "https://" + DEVELOP_API_DOMAIN + "/"
                                    + API_ID
                                    + "/calendar/contact/getDomainContact/v1?"
                                      "account=" + ADMIN_ACCOUNT,
                "time_zone_url": "https://" + DEVELOP_API_DOMAIN + "/r/"
                                 + API_ID
                                 + "/organization/v2/domains/DOMAIN_ID"
                                   "/users/EXTERNAL_KEY/g11ns"
            },
            "auth_url": "https://" + AUTH_DOMAIN + "/b/" + API_ID
                        + "/server/token?grant_type=urn%3Aietf%3Aparams%3Aoauth"
                          "%3Agrant-type%3Ajwt-bearer&assertion="
        }

OPEN_API = {
        "_info": "nwetest.com",
        "apiId": API_ID,
        "consumerKey": CONSUMER_KEY,
        "service_consumerKey": SERVICE_CONSUMER_KEY
    }

DB_CONFIG = {
    "host": DB_HOST,
    "port": DB_PORT,
    "name": DB_NAME,
    "user": DB_USER,
    "password": DB_PASSWORD,
    "ssl": DB_SSLMODE
}

FILE_SYSTEM = {
    "cache_dir": ABSDIR_OF_ROOT+"/cache",
    "image_dir": ABSDIR_OF_ROOT+"/image",
}
