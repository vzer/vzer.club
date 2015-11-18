#!/usr/bin/env python
#coding=utf-8
__author__ = 'vzer'

from flask import config

class Base_Config(object):
    #app.config
    DEBUG=True
    CSRF_ENABLED = True
    SECRET_KEY=""
    POST_PRE_PAGE=8

    #mysql.config
    MYSQL_DB = ""
    MYSQL_USER = ""
    MYSQL_PASS = ""
    MYSQL_HOST = ""
    MYSQL_PORT = ""

    SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@%s:%s/%s' \
                          % (MYSQL_USER, MYSQL_PASS,
                             MYSQL_HOST, MYSQL_PORT, MYSQL_DB)
