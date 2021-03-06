#!/bin/env python
# -*- encoding: utf-8 -*-

# from gevent import monkey
# monkey.patch_all()
"""
main function for calender
"""
import signal
from daemonize import Daemonize
from tornado.options import define, options
from calender.calender import *
from calender.settings import *


define("daemonize", default=False, help="daemon mode")
define("pidfile", default=CALENDER_PID_FILE,
       help="the path of pid file, default None")


if __name__ == "__main__":
    options.parse_command_line()

    signal.signal(signal.SIGPIPE, signal.SIG_IGN)
    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGQUIT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGHUP, sig_handler)

    if options.daemonize:
        daemon = Daemonize(app="calender", action=start_calender,
                           pid=options.pidfile)
        daemon.start()
    else:
        start_calender()
