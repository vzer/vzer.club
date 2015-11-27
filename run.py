#!/usr/bin/env python
#coding=utf-8
__author__ = 'vzer'

from flask import Flask
from flask_login import LoginManager
from develop_config import Develop_Config
from flask_sqlalchemy import SQLAlchemy
from  flask_restful import Resource,Api


app = Flask(__name__)
lm=LoginManager(app)
lm.init_app(app)
lm.login_view="login"
lm.login_message="此操作未授权，请登录系统"
app.config.from_object(Develop_Config)
db=SQLAlchemy(app)
api=Api(app)


from adminview import *
from view import *
from restful import *

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8081)

