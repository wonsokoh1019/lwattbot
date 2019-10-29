#!/bin/env python
# -*- coding: utf-8 -*-

import logging
from calender.model.postgreSqlPool import PostGreSql
from psycopg2.errors import DuplicateTable, DuplicateObject

LOGGER = logging.getLogger("calender")


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

    post_gre = PostGreSql()

    try:
        post_gre.cursor.execute(status_type_sql)
        post_gre.cursor.execute(process_type_sql)
        post_gre.cursor.execute(create_sql)
        post_gre.conn.commit()
    except DuplicateObject as ex:
        LOGGER.info("type's has created. %s", str(ex))
        post_gre.conn.rollback()
    except DuplicateTable as ex:
        LOGGER.info("table's has created. %s", str(ex))
        post_gre.conn.rollback()
    finally:
        post_gre.close()
    return True


def insert_replace_status_by_user_date(account, date, status, process=None):
    if status is None:
        return False

    insert_sql = "INSERT INTO bot_process_status(account, cur_date, status)" \
                 " VALUES('%s', '%s', '%s') ON CONFLICT(account, cur_date) " \
                 "DO UPDATE SET status='%s', update_time=now()" % \
                 (account, date, status, status)
    if process is not None:
        insert_sql = "INSERT INTO bot_process_status(" \
                     "account, cur_date, status, process) " \
                     "VALUES('%s', '%s', '%s', '%s') " \
                     "ON CONFLICT(account, cur_date) " \
                     "DO UPDATE SET " \
                     "status='%s', process='%s', update_time=now()" % \
                     (account, date, status, process, status, process)

    post_gre = PostGreSql()

    try:
        post_gre.cursor.execute(insert_sql)
        post_gre.conn.commit()
    finally:
        post_gre.close()


def set_status_by_user_date(account, date, status=None, process=None):

    condition = "WHERE account='%s' and cur_date='%s'" % (account, date)

    update_sql = "UPDATE bot_process_status SET update_time=now()"
    if status is not None:
        update_sql = "%s , status='%s'" % (update_sql, status,)
    if process is not None:
        update_sql = "%s , process='%s'" % (update_sql, process,)

    update_sql = "%s %s" % (update_sql, condition,)

    post_gre = PostGreSql()
    try:
        post_gre.cursor.execute(update_sql)
        post_gre.conn.commit()
    finally:
        post_gre.close()


def get_status_by_user(account, date):

    select_sql = "SELECT status, process " \
                 "FROM bot_process_status " \
                 "WHERE account='%s' and cur_date='%s'" \
                 % (account, date)

    post_gre = PostGreSql()

    row = None
    try:
        post_gre.cursor.execute(select_sql)
        rows = post_gre.cursor.fetchall()
        if rows is not None and len(rows) == 1:
            # ['status', 'process']
            row = rows[0]
    finally:
        post_gre.close()

    return row


def delete_status_by_user_date(account, date):
    delete_status_sql = "UPDATE bot_process_status SET status=NULL, " \
                        "update_time=now() " \
                        "WHERE account='%s' and cur_date='%s'" % \
                        (account, date)

    post_gre = PostGreSql()
    try:
        post_gre.cursor.execute(delete_status_sql)
        post_gre.conn.commit()
    finally:
        post_gre.close()


def clean_status_by_user(account, date):
    delete_sql = "DELETE FROM bot_process_status " \
                 "WHERE account='%s' and cur_date='%s' " % (account, date)

    post_gre = PostGreSql()
    try:
        post_gre.cursor.execute(delete_sql)
        post_gre.conn.commit()
    finally:
        post_gre.close()
