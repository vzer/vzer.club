#!/usr/bin/env python
#coding=utf-8
__author__ = 'vzer'

from base_config import Base_Config

class Develop_Config(Base_Config):
    #app.config
    SECRET_KEY="vzer_blog_1589"
    POST_PRE_PAGE=6
    REGISTERCODE="cheurbim_1589"
    DEBUG = False

    #mysql config
    MYSQL_DB = "vzerblog"
    MYSQL_USER = "vzer"
    MYSQL_PASS = "wwwlin123"
    MYSQL_HOST = "192.168.1.246"
    MYSQL_PORT = int("3306")

    SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@%s:%s/%s' \
                          % (MYSQL_USER, MYSQL_PASS,
                             MYSQL_HOST, MYSQL_PORT, MYSQL_DB)
    SQLALCHEMY_ECHO=True

    #mail config

    ADMINS = ["zhangcunlei@xiniunet.com",]

    MAIL_SERVER = u'smtp.xiniunet.com'
    MAIL_USERNAME = u'zhangcunlei@xiniunet.com'
    MAIL_PASSWORD = u'wwwlin123!'
    DEFAULT_MAIL_SENDER = u'zhangcunlei@xiniunet.com'
    MAIL_USE_TLS=False
    MAIL_USE_SSL=False


    #log config

    DEBUG_LOG = 'logs/debug.log'
    ERROR_LOG = 'logs/error.log'