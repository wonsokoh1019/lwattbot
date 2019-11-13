#!/bin/bash python
# -*- coding: utf-8 -*-
"""
launch calender
"""
import os
import logging
import logging.handlers
import asyncio
import uvloop
import json
import tornado.ioloop
import tornado.web
import tornado.httpserver
from tornado.httpclient import AsyncHTTPClient
from tornado.options import define, options
from calender.externals.richmenu import init_rich_menu
from calender.common import global_data
from calender.externals.calender_req import init_calender
from calender.constant import API_BO, LOCAL
from calender.model.initStatusDBHandle import insert_init_status, \
    get_init_status

import psutil

import calender.router
import calender.contextlog
from calender.safetimedrotatingfilehandler import SafeTimedRotatingFileHandler
from calender.settings import CALENDER_PORT, CALENDER_LOG_FMT, \
    CALENDER_LOG_LEVEL, CALENDER_LOG_FILE, CALENDER_LOG_ROTATE

define("port", default=CALENDER_PORT, help="server listen port. "
                                           "default 8080")
define("workers", default=0, help="the count of workers. "
                                  "default the same as cpu cores")
define("logfile", default=None, help="the path for log")

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def sig_handler(sig, _):
    """
    signal handler
    """
    print("sig %s received" % str(sig))
    try:
        parent = psutil.Process(os.getpid())
        children = parent.children()
        for process in children:
            process.send_signal(sig)
    except (psutil.NoSuchProcess, psutil.ZombieProcess,
            psutil.AccessDenied) as ex:
        print(str(ex))
    tornado.ioloop.IOLoop.instance().add_callback(kill_server)


def kill_server():
    """
    stop the ioloop
    """
    asyncio.get_event_loop().stop()


def init_logger():
    """
    init logger setting
    """
    formatter = logging.Formatter(CALENDER_LOG_FMT)
    calender_log = logging.getLogger("calender")
    file_handler = SafeTimedRotatingFileHandler(filename=CALENDER_LOG_FILE,
                                                when=CALENDER_LOG_ROTATE,)
    file_handler.setFormatter(formatter)

    calender_log.setLevel(CALENDER_LOG_LEVEL)
    file_handler.addFilter(calender.contextlog.RequestContextFilter())
    calender_log.addHandler(file_handler)

    # add app/gen ERROR log
    logging.getLogger("tornado.application").addHandler(file_handler)
    logging.getLogger("tornado.general").addHandler(file_handler)


def check_init_bot():
    extra = get_init_status("bot_no")
    if extra is None:
        raise Exception("bot no init failed.")
    global_data.set_value("bot_no", extra)


def init_rich_menu_first():
    extra = get_init_status("rich_menu")

    if extra is None:
        rich_menus = init_rich_menu(LOCAL)
        insert_init_status("rich_menu", json.dumps(rich_menus))
    else:
        rich_menus = json.loads(extra)

    if rich_menus is None:
        raise Exception("init rich menu failed.")
    else:
        for key in rich_menus:
            global_data.set_value(key, rich_menus[key])


def init_calender_first():
    calender_id = get_init_status("calender")
    if calender_id is None:
        calender_id = init_calender()
        insert_init_status("calender", calender_id)

    global_data.set_value(API_BO["calendar"]["name"], calender_id)


def start_calender():
    """
    the calender launch code
    """
    server = tornado.httpserver.HTTPServer(calender.router.getRouter())

    server.bind(options.port)
    server.start(1)

    init_logger()
    check_init_bot()
    init_rich_menu_first()
    init_calender_first()

    asyncio.get_event_loop().run_forever()
    server.stop()
    asyncio.get_event_loop().close()

    print("exit...")
