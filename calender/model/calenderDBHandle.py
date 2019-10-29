#!/bin/env python
# -*- coding: utf-8 -*-
import logging
from calender.model.postgreSqlPool import PostGreSql
from psycopg2.errors import DuplicateTable

LOGGER = logging.getLogger("calender")


# create calender table.
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

    post_gre = PostGreSql()

    try:
        post_gre.cursor.execute(create_sql)
        post_gre.cursor.execute(index_sql)
        post_gre.conn.commit()
    except DuplicateTable as ex:
        LOGGER.info("table's has created. %s", str(ex))
        post_gre.conn.rollback()
    finally:
        post_gre.close()

    return True


# inset schedule
def set_schedule_by_user(schedule_id, account, date,  begin, end):
    insert_sql = "INSERT INTO bot_calender_record(schedule_id, account, " \
                 "cur_date, begin_time, end_time) " \
                 "VALUES('%s', '%s', '%s', %d, %d)" \
                 % (schedule_id, account, date, begin, end)

    post_gre = PostGreSql()

    try:
        post_gre.cursor.execute(insert_sql)
        post_gre.conn.commit()
    finally:
        post_gre.close()


# update schedule
def get_schedule_by_user(account, date):
    select_sql = "SELECT schedule_id, begin_time " \
                 "FROM bot_calender_record " \
                 "WHERE account='%s' and cur_date='%s'" \
                 % (account, date)

    post_gre = PostGreSql()

    row = None
    try:
        post_gre.cursor.execute(select_sql)
        rows = post_gre.cursor.fetchall()
        if rows is not None and len(rows) == 1:
            # ["schedule_id", "begin_time"]
            row = rows[0]
    finally:
        post_gre.close()

    return row


def modify_schedule_by_user(schedule_id, end):
    select_sql = "UPDATE bot_calender_record " \
                 "SET end_time=%d, update_time=now()" \
                 "WHERE schedule_id='%s'" \
                 % (end, schedule_id)

    post_gre = PostGreSql()

    try:
        post_gre.cursor.execute(select_sql)
        post_gre.conn.commit()
    finally:
        post_gre.close()


def clean_schedule_by_user(account, date):
    delete_sql = "DELETE FROM bot_calender_record " \
                 "WHERE account='%s' and cur_date='%s'" \
                 % (account, date)

    post_gre = PostGreSql()

    try:
        post_gre.cursor.execute(delete_sql)
        post_gre.conn.commit()
    finally:
        post_gre.close()
