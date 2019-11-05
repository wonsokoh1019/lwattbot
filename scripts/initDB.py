#!/bin/env python
# -*- coding: utf-8 -*-
import sys
import json
import psycopg2
import psycopg2.extras as extras
from psycopg2.errors import DuplicateTable, DuplicateObject
sys.path.append('./')
from conf.config import *

# create calender table
def create_calender_table():
    create_sql = "CREATE TABLE IF NOT EXISTS bot_calender_record(" \
                 "schedule_id  varchar(128)      NOT NULL, " \
                 "account      varchar(64)       NOT NULL, " \
                 "cur_date     date              NOT NULL, " \
                 "begin_time   bigint            NOT NULL, " \
                 "end_time     bigint            NOT NULL, " \
                 "create_time  timestamp         NOT NULL " \
                 "default current_timestamp, " \
                 "update_time  timestamp         NOT NULL " \
                 "default current_timestamp, " \
                 "PRIMARY KEY (schedule_id)" \
                 ");"

    index_sql = "CREATE UNIQUE INDEX account_time " \
                "ON bot_calender_record(account, cur_date);"

    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                            password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()
    with conn:
        with cur:
            try:
                cur.execute(create_sql)
                cur.execute(index_sql)
            except DuplicateTable:
                conn.rollback()

        # create init status table
def create_init_status():
    create_sql = "CREATE TABLE IF NOT EXISTS system_init_status(" \
                 "action       varchar(64)   NOT NULL, " \
                 "extra      varchar(128)     DEFAULT NULL, " \
                 "create_time  TIMESTAMP     NOT NULL " \
                 "DEFAULT      CURRENT_TIMESTAMP, " \
                 "update_time  TIMESTAMP         NOT NULL " \
                 "default      CURRENT_TIMESTAMP, " \
                 "PRIMARY KEY (action)" \
                 ");"

    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                            password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()
    with conn:
        with cur:
            cur.execute(create_sql)

# create status tables
def create_process_status_table():
    status_type_sql = "CREATE TYPE m_status AS " \
                      "ENUM('none', 'wait_in', " \
                      "'in_done', 'wait_out', 'out_done');"

    process_type_sql = "CREATE TYPE m_process AS " \
                       "ENUM('none', 'sign_in_done', 'sign_out_done');"

    create_sql = "CREATE TABLE IF NOT EXISTS bot_process_status(" \
                 "account      varchar(64)   NOT NULL, " \
                 "cur_date     date          NOT NULL, " \
                 "status       m_status      DEFAULT NULL, " \
                 "process      m_process     DEFAULT NULL, " \
                 "create_time  timestamp     NOT NULL " \
                 "default current_timestamp, " \
                 "update_time  timestamp         NOT NULL " \
                 "default current_timestamp, " \
                 "PRIMARY KEY (account, cur_date)" \
                 ");"

    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                            password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()
    with conn:
        with cur:
            try:
                cur.execute(status_type_sql)
                cur.execute(process_type_sql)
                cur.execute(create_sql)
            except DuplicateObject:
                conn.rollback()
            except DuplicateTable as ex:
                conn.rollback()

def main():
    create_calender_table()
    create_init_status()
    create_process_status_table()

if __name__ == "__main__":
    main()
