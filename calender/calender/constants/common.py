#!/bin/env python
# -*- coding: utf-8 -*-
import os

# root path
ABSDIR_OF_SELF = os.path.dirname(os.path.abspath(__file__))
ABSDIR_OF_PARENT = os.path.dirname(ABSDIR_OF_SELF)
ABSDIR_OF_ROOT = os.path.dirname(ABSDIR_OF_PARENT)

# account
LANG = "kr"    # ["kr"|"en"|"jp"]
ADMIN_ACCOUNT = "admin@krbot.com"
RECEIVE_ACCOUNT = "admin02@nwetest.com"
DOMAIN_ID = 18644

# api
API_ID = "kr1EHAIjvfJVz"
CONSUMER_KEY = "To8SnC7sLIAv8GjqXZhO"

"""
TOKEN = "AAAA9iXhCP9TqAVK2ic1mYIEybAyrWVYfg9q/GwxmwkmqneLCYFcR3VhWwfcOuHwh" \
        "UBu7YCTASpWUpqBZqC38TgiraxVgRNv9HgA+Kj17mTE2XCmqxNMyaTLVQ6hrwck4J" \
        "qYqsQ8ldBUd8dEp2i7CqkbPf7sCWuV6HK6VLR6OcmG9xCZMbhL1hnuvvKywWeJun+" \
        "aLfpF4weoF/kF7LvTOicloLBd+XieqNTY+ChsdMYKP3VeeYRwE6mWGON9qWfJ5VqK" \
        "HDEiaF7tdBWKNKM12qtk9yiyZ+CMf8kfVFPnBHVgX0AZjrfiZXAo2qnh0AF/J0MdM" \
        "5EggY9vmmcOpc9/FmHfPFo="
"""
SERVER_ID = "96460cc1e778402dae5bfe35fa97ce76"
PRIVATE_KEY_NAME = "private_20191017164308.key"

TOKEN = None
# LOCAL ADDRESS
# LOCAL_ADDRESS = "http://10.105.180.133:8080/"
LOCAL_ADDRESS = "https://10.105.180.133:8080/"

# DB config
DB_HOST = "10.106.151.241"
DB_PORT = "5432"
DB_NAME = "dbwyc"
DB_USER = "dbtest"
DB_PASSWORD = "123456"
DB_SSLMODE = "prefer"

# domain
STORAGE_DOMAIN = "alpha-storage.worksmobile.com"
AUTH_DOMAIN = "alpha-auth.worksmobile.com"
DEVELOP_API_DOMAIN = "alpha-apis.worksmobile.com"
