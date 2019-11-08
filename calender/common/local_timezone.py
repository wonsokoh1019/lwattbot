#!/bin/env python
# -*- coding: utf-8 -*-

from calender.common.global_data import get_value, set_value
from datetime import datetime, timedelta, timezone
from calender.externals.calender_req import get_time_zone
import pytz
import json


def get_offset_by_timezone(time_zone):
    offset = datetime.now(pytz.timezone(time_zone)).utcoffset().total_seconds()
    offset_hour = offset / 3600
    offset_min = (offset % 3600)/60
    return offset_hour, offset_min


def get_tz():
    offset_time_zone = get_value("offsetTimeZone", None)
    if offset_time_zone is None:
        return None
    return json.loads(offset_time_zone)


def set_tz():
    time_zone = get_time_zone()
    if time_zone is None:
        raise Exception("get timezone failed.")

    hours, minutes = get_offset_by_timezone(time_zone)

    offset_time_zone = {"hours": hours, "minutes": minutes}
    set_value("offsetTimeZone", json.dumps(offset_time_zone))

    return offset_time_zone


def local_date_time(time=None):
    offset_time_zone = get_tz()
    if offset_time_zone is None:
        offset_time_zone = set_tz()
    hours = offset_time_zone.get("hours", None)
    minutes = offset_time_zone.get("minutes", None)
    if time is not None:
        date_time = datetime.utcfromtimestamp(time)
        utc_dt = date_time.replace(tzinfo=timezone.utc)
        delta = timedelta(hours=int(hours), minutes=int(minutes))
        return utc_dt.astimezone(timezone(delta))

    utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
    delta = timedelta(hours=hours, minutes=minutes)
    return utc_dt.astimezone(timezone(delta))
