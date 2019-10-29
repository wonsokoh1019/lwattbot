#!/bin/env python3
# -*- coding: utf-8 -*-
"""
the url to handler route
"""
import tornado.web
from calender.callbackHandler import CallbackHandler
from calender.StaticImageHandler import StaticImageHandler
from calender.hellohandler import HelloHandler


def getRouter():
    """
    get the app with route info
    """
    return tornado.web.Application([
        (r"/callback", CallbackHandler),
        (r'/static/[^# ]*', StaticImageHandler),
        (r'/hello', HelloHandler),
    ])
