#!/bin/env python
# -*- coding: utf-8 -*-
import sys
import json
import psycopg2
import requests
import python_jwt as jwt
import jwcrypto.jwk as jwk
import datetime
import psycopg2.extras as extras
from psycopg2.errors import DuplicateTable
sys.path.append('./')
from calender.constant import PRIVATE_KEY_PATH, DEVELOP_API_DOMAIN, API_BO
from conf.config import *

callback_address = LOCAL_ADDRESS + "callback"
photo_url = LOCAL_ADDRESS + "static/icon.png"
key_path = PRIVATE_KEY_PATH
auth_url = API_BO["auth_url"]

def create_tmp_token():
    with open(key_path, "rb") as _file:
        key = _file.read()
        private_key = jwk.JWK.from_pem(key)
        payload = {"iss": SERVER_ID}
        my_token = jwt.generate_jwt(payload, private_key, 'RS256',
                                 datetime.timedelta(minutes=5))
        return my_token
    return None


def generate_token():
    tmp_token = create_tmp_token()
    if tmp_token is None:
        raise Exception("generate tmp token failed.")
    my_headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "charset": "UTF-8"
    }
    url = auth_url + tmp_token
    response = requests.post(url, headers=my_headers)
    if response.status_code != 200:
        raise Exception("generate token failed.")

    content = json.loads(response.content)
    tmp_token = content.get("access_token", None)
    if tmp_token is None:
        raise Exception("response token is None.")

    return tmp_token

def headers():
    if TOKEN is None and SERVER_ID is None:
        raise Exception("token and server id is valid.")
    token = TOKEN
    if TOKEN is None:
        token = generate_token()
    my_headers = {
        "consumerKey": CONSUMER_KEY,
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json",
        "charset": "UTF-8"
    }
    return my_headers


def create_bot(photo_address):
    url = "https://" + DEVELOP_API_DOMAIN + "/r/" + API_ID + "/message/v1/bot"
    data = {
        "name": "근태관리 봇",
        "i18nNames": [
            {
                "language": "ko_KR",
                "name": "근태관리 봇"
            },
            {
                "language": "ja_JP",
                "name": "勤怠管理Bot"
            },
            {
                "language": "en_US",
                "name": "Attendance management bot"
            }
        ],
        "photoUrl": photo_address,
        "i18nPhotoUrls": [
            {
                "language": "ko_KR",
                "photoUrl": photo_address
            },
            {
                "language": "ja_JP",
                "photoUrl": photo_address
            },
            {
                "language": "en_US",
                "photoUrl": photo_address
            }
        ],
        "description": "근태관리 봇",
        "i18nDescriptions": [
            {
                "language": "ko_KR",
                "description": "근태관리 봇"
            },
            {
                "language": "ja_JP",
                "description": "勤怠管理Bot"
            },
            {
                "language": "ja_JP",
                "description": "Attendance management bot"
            }
        ],
        "managers": [ADMIN_ACCOUNT],
        "submanagers": [],
        "useGroupJoin": False,
        "useDomainScope": False,
        "useCallback": True,
        "callbackUrl": callback_address,
        "callbackEvents": ["text", "location", "sticker", "image"]
    }

    r = requests.post(url, data=json.dumps(data), headers=headers())
    if r.status_code != 200:
        print(r.text)
        print(r.content)
        return None
    tmp = r.json()
    print(tmp)
    return tmp["botNo"]


def add_domain(bot_no):
    url = "https://" + DEVELOP_API_DOMAIN + "/r/" + API_ID + "/message/v1/bot/" \
          + str(bot_no) + "/domain/" + str(DOMAIN_ID)
    data = {"usePublic": True, "usePermission": False}
    r = requests.post(url, data=json.dumps(data), headers=headers())
    print(r.json())

def check_bot_in_db():

    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                            password=DB_PASSWORD, host=DB_HOST,
                            port=DB_PORT, sslmode=DB_SSLMODE)
    cur = conn.cursor()

    select_sql = "SELECT extra FROM system_init_status WHERE action='bot_no'"
    with conn:
        with cur:
            try:
                cur.execute(select_sql)
                rows = cur.fetchall()
                if rows is not None and len(rows) == 1:
                    extra = rows[0][0]
                    return extra
            except Exception as ex:
                print ("table's created failed. %s" % (str(ex),))
                return None
    return None

def add_bot_in_db(bot_no):

    insert_sql = "INSERT INTO system_init_status(action, extra) " \
                 "VALUES('%s', '%s') ON CONFLICT(action) " \
                 "DO UPDATE SET extra='%s', update_time=now()" % \
                 ("bot_no", str(bot_no), str(bot_no))

    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                            password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()
    with conn:
        with cur:
            cur.execute(insert_sql)

    return True

def main():
    bot_no = check_bot_in_db()
    if bot_no is not None:
        print("bot no has created. bot_no:%s" % (bot_no,))
        return

    bot_no = create_bot(photo_url)
    add_domain(bot_no)
    print("photo:%s" % (photo_url,))
    print("callback:%s" % (callback_address,))
    if bot_no is not None:
        add_bot_in_db(bot_no)


if __name__ == "__main__":
    main()
