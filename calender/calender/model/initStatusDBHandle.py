#!/bin/env python
# -*- coding: utf-8 -*-
import logging
from calender.model.postgreSqlPool import PostGreSql
from psycopg2.errors import DuplicateTable


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

    post_gre = PostGreSql()
    try:
        post_gre.cursor.execute(create_sql)
    except DuplicateTable as ex:
        post_gre.conn.rollback()
        LOGGER.info("table's has created. %s", str(ex))
    finally:
        post_gre.close()
    return True


def insert_init_status(action, extra):
    insert_sql = "INSERT INTO system_init_status(action, extra) " \
                 "VALUES('%s', '%s') ON CONFLICT(action) " \
                 "DO UPDATE SET extra='%s', update_time=now()" % \
                 (action, extra, extra)

    post_gre = PostGreSql()
    try:
        post_gre.cursor.execute(insert_sql)
        post_gre.conn.commit()
    except DuplicateTable as ex:
        post_gre.conn.rollback()
        LOGGER.info("table's has created. %s", str(ex))
    finally:
        post_gre.close()
    return True


def update_init_status(action, extra):
    update_sql = "UPDATE system_init_status SET update_time=now()," \
                 "extra='%s' " \
                 "WHERE action='%s'" % (extra, action)

    post_gre = PostGreSql()
    try:
        post_gre.cursor.execute(update_sql)
        post_gre.conn.commit()
    finally:
        post_gre.close()


def get_action_info(action):
    select_sql = "SELECT extra " \
                 "FROM system_init_status WHERE action='%s'" % (action,)

    post_gre = PostGreSql()
    extra = None
    try:
        post_gre.cursor.execute(select_sql)
        rows = post_gre.cursor.fetchall()
        if rows is not None and len(rows) == 1:
            extra = rows[0][0]
    finally:
        post_gre.close()
    return extra


def delete_action_info(action):
    select_sql = "DELETE FROM system_init_status WHERE action='%s'" % (action,)
    post_gre = PostGreSql()
    extra = None
    try:
        post_gre.cursor.execute(select_sql)
        post_gre.conn.commit()
    finally:
        post_gre.close()
    return extra
