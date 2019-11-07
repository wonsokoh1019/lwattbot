#!/bin/env python3
# -*- coding: utf-8 -*-
"""
the url to handler route
"""
import tornado.web
from calender.callbackHandler import CallbackHandler
from calender.hellohandler import HelloHandler
from calender.constant import FILE_SYSTEM


def getRouter():
    """
    get the app with route info
    """
    return tornado.web.Application([
        (r"/callback", CallbackHandler),
        (r'/static/([a-zA-Z0-9\&%_\./-~-]*.(png|PNG))',
            tornado.web.StaticFileHandler, 
            {"path": FILE_SYSTEM["image_dir"]}),
        (r'/hello', HelloHandler),
    ])
