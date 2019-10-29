#!/bin/env python
# -*- coding: utf-8 -*-

import requests
import logging
from calender.common.token import generate_token
from calender.common.globalData import get_value, set_value
from calender.constant import IP_TOKEN


def refresh_token():
    if IP_TOKEN is not None:
        my_token = IP_TOKEN
    else:
        my_token = generate_token()
        set_value("token", my_token)
    return my_token


def get_token():
    return set_value("token", None)


def replace_url_bot_no(url):
    bot_no = get_value("bot_no", None)
    if bot_no is None:
        return None

    url = url.replace("_BOT_NO_", bot_no)
    return url


def auth_post(url, data=None,  headers=None, files=None,
              params=None, json=None, refresh_token_flag=False):
    if headers is not None and not refresh_token_flag:
        my_token = get_token()
        if my_token is None:
            my_token = refresh_token()

        headers["Authorization"] = "Bearer " + my_token
        response = requests.post(url, data=data, headers=headers,
                                 files=files, params=params, json=json)

        if response.status_code == 401 or response.status_code == 403:
            my_token = refresh_token()
            headers["Authorization"] = "Bearer " + my_token
            response = requests.post(url, data=data, headers=headers,
                                     files=files, params=params, json=json)
        return response
    else:
        if refresh_token_flag and headers is not None:
            my_token = refresh_token()
            headers["Authorization"] = "Bearer " + my_token
        return requests.post(url, data=data, headers=headers,
                             files=files, params=params, json=json)

    return None


def auth_get(url, headers=None, refresh_token_flag=False):
    if headers is not None and not refresh_token_flag:
        my_token = get_token()
        if my_token is None:
            my_token = refresh_token()

        headers["Authorization"] = "Bearer " + my_token
        response = requests.get(url, headers=headers)

        if response.status_code == 401 or response.status_code == 403:
            my_token = refresh_token()
            headers["Authorization"] = "Bearer " + my_token
            response = requests.get(url, headers=headers)
        return response
    else:
        if refresh_token_flag and headers is not None:
            my_token = refresh_token()
            headers["Authorization"] = "Bearer " + my_token
        return requests.get(url, headers=headers)

    return None


def auth_del(url, headers=None, refresh_token_flag=False):
    if headers is not None and not refresh_token_flag:
        my_token = get_token()
        if my_token is None:
            my_token = init_token()

        headers["Authorization"] = "Bearer " + my_token
        response = requests.delete(url, headers=headers)

        if response.status_code == 401 or response.status_code == 403:
            my_token = refresh_token()
            headers["Authorization"] = "Bearer " + my_token
            response = requests.delete(url, headers=headers)
        return response
    else:
        if refresh_token_flag and headers is not None:
            my_token = refresh_token()
            headers["Authorization"] = "Bearer " + my_token
        return requests.delete(url, headers=headers)

    return None
