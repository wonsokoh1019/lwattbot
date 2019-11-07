#!/bin/env python
# -*- coding: utf-8 -*-
"""
internal hello
"""
import json
import logging
import tornado.web
from calender.checkAndHandleActions import *

LOGGER = logging.getLogger("calender")


class CallbackHandler(tornado.web.RequestHandler):
    """
    /internal/hello
    """

    @tornado.gen.coroutine
    def post(self):
        """
        support post
        """

        path = self.request.uri
        LOGGER.info("request para path:%s", path)
        try:
            body = json.loads(self.request.body)
        except Exception:
            raise tornado.web.HTTPError(403, "boy is not json.")

        LOGGER.info("request para body:%s", self.request.body)
        checker = CheckAndHandleActions()
        yield checker.execute(body)

        LOGGER.info("request para code:%d message:%s", checker.code, checker.message)
        if checker.code is None:
            raise tornado.web.HTTPError(403, checker.message)

        if not checker.code:
            raise tornado.web.HTTPError(500, checker.message)

        self.finish()
