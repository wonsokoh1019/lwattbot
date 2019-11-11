#!/bin/env python
# -*- coding: utf-8 -*-
import io
import logging
import json
import pytz
import uuid
import tornado.gen
from tornado.web import HTTPError
from datetime import datetime, timezone
from icalendar import Calendar, Event, Timezone, TimezoneStandard
from calender.common.utils import auth_get, auth_post, auth_put
from calender.common.local_timezone import load_time_zone
from calender.common.local_external_key import load_external_key
from calender.constant import API_BO, OPEN_API, ADMIN_ACCOUNT, DOMAIN_ID, LOCAL
from calender.common.global_data import get_value

LOGGER = logging.getLogger("calender")


def create_headers():
    headers = API_BO["headers"]
    headers["consumerKey"] = OPEN_API["consumerKey"]
    return headers


def make_icalender_data(uid, summary, current, end, begin, account_id, create_flag=False):
    cal = Calendar()
    cal.add('PRODID', 'Works sample bot Calendar')
    cal.add('VERSION', '2.0')

    tz = load_time_zone()
    standard = TimezoneStandard()
    standard.add('DTSTART', datetime(1970, 1, 1, 0, 0, 0,
                                     tzinfo=pytz.timezone(tz)))
    standard.add('TZOFFSETFROM', current.utcoffset())
    standard.add('TZOFFSETTO', current.utcoffset())
    standard.add('TZNAME', current.tzname())

    tz = Timezone()
    tz.add_component(standard)
    tz.add('TZID', tz)

    event = Event()
    event.add('UID', uid)

    if create_flag:
        event.add('CREATED', current)

    event.add('DESCRIPTION', account_id)
    event.add('ATTENDEE', account_id)
    event.add('SUMMARY', summary)
    event.add('DTSTART', begin)
    event.add('DTEND', end)
    event.add('LAST-MODIFIED', current)
    event.add('DTSTAMP', current)

    cal.add_component(event)
    cal.add_component(tz)
    schedule_local_string = bytes.decode(cal.to_ical())
    LOGGER.info("schedule:%s", schedule_local_string)
    return schedule_local_string


def create_calender():
    names = {
        "kr": "근태관리 봇",
        "jp": "勤怠管理Bot",
        "en": "Attendance management bot"
    }

    body = {
        "name": names[LOCAL],
        "description": names[LOCAL],
        "invitationUserList": [{
            "email": ADMIN_ACCOUNT,
            "actionType": "insert",
            "roleId": 2
        }]
    }

    headers = create_headers()
    url = API_BO["calendar"]["create_calender_url"]
    url = url.replace("_EXTERNAL_KEY_", load_external_key())
    LOGGER.info("create calender. url:%s body:%s", url, str(body))

    response = auth_post(url, data=json.dumps(body), headers=headers)
    if response.status_code != 200:
        LOGGER.error("create calender failed. url:%s text:%s body:%s",
                    url, response.text, response.content)
        raise Exception("create calender id. http response code error.")

    LOGGER.info("create calender id. url:%s txt:%s body:%s",
                url, response.text, response.content)
    tmp_req = json.loads(response.content)
    if tmp_req["result"] != "success":
        LOGGER.error("create calender failed. url:%s text:%s body:%s",
                     url, response.text, response.content)
        raise Exception("create calender id. response no success.")
    return tmp_req["returnValue"]


def create_schedule(current, end, begin, account_id):
    summarys = {
        "kr": "출근시간",
        "jp": "出勤時間",
        "en": "Clock-in time"
    }

    uid = str(uuid.uuid4()) + account_id
    schedule_data = make_icalender_data(uid, summarys[LOCAL], current,
                                        end, begin, account_id, True)
    body = {
        "ical": schedule_data
    }

    calender_id = get_value(API_BO["calendar"]["name"], None)
    if calender_id is None:
        LOGGER.error("get calender from cached failed.")
        raise HTTPError(500, "internal error. get calender is failed.")

    headers = create_headers()
    url = API_BO["calendar"]["create_schedule_url"]
    url = url.replace("_EXTERNAL_KEY_", load_external_key())
    url = url.replace("_CALENDER_ID_", calender_id)

    response = auth_post(url, data=json.dumps(body), headers=headers)
    if response.status_code != 200:
        LOGGER.error("create schedules failed. url:%s text:%s body:%s",
                    url, response.text, response.content)
        raise HTTPError(500, "internal error. create schedule http code error.")

    tmp_req = json.loads(response.content)
    if tmp_req["result"] != "success":
        LOGGER.error("create schedule failed. url:%s text:%s body:%s",
                     url, response.text, response.content)
        raise HTTPError(500, "internal error. http response error.")

    LOGGER.info("create schedule. url:%s text:%s body:%s",
                 url, response.text, response.content)

    return_value = tmp_req.get("returnValue", None)
    if return_value is None:
        LOGGER.error("create schedule failed. url:%s text:%s body:%s",
                     url, response.text, response.content)
        raise HTTPError(500, "internal error. create schedule content error.")

    schedule_uid = return_value.get("icalUid", None)
    if schedule_uid is None:
        LOGGER.error("create schedule failed. url:%s text:%s body:%s",
                     url, response.text, response.content)
        raise HTTPError(500, "internal error. create schedule content error.")
    return schedule_uid


def modify_schedule(calender_uid, current, end, begin, account_id):
    summarys = {
        "kr": "근무시간",
        "jp": "勤務時間",
        "en": "Working hours"
    }

    calender_data = make_icalender_data(calender_uid, summarys[LOCAL],
                                        current, end, begin, account_id)
    body = {
        "ical": calender_data
    }

    calender_id = get_value(API_BO["calendar"]["name"], None)
    if calender_id is None:
        LOGGER.error("get calender from cached failed.")
        raise HTTPError(500, "internal error. get calender is failed.")

    url = API_BO["calendar"]["modify_schedule_url"]
    url = url.replace("_EXTERNAL_KEY_", load_external_key())
    url = url.replace("_CALENDER_ID_", calender_id)
    url = url.replace("_CALENDER_UUID_", calender_uid)

    headers = create_headers()
    response = auth_put(url, data=json.dumps(body), headers=headers)
    if response.status_code != 200:
        LOGGER.error("modify schedules failed. url:%s text:%s body:%s",
                     url, response.text, response.content)
        raise HTTPError(500,
                        "internal error. create schedule http code error.")

    LOGGER.info("modify schedules. url:%s text:%s body:%s",
                 url, response.text, response.content)

    tmp_req = json.loads(response.content)
    if tmp_req["result"] != "success":
        LOGGER.error("modify schedule failed. url:%s text:%s body:%s",
                     url, response.text, response.content)
        raise HTTPError(500, "internal error. http response error.")


def init_calender():
    calender_id = create_calender()
    if calender_id is None:
        raise Exception("init calender failed.")
    return calender_id
