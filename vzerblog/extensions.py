#!/usr/bin/env python
#coding=utf-8
__author__ = 'vzer'

from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_restful import Api
from flask_mail import Mail
from adminview import MyAdminIndexView

__all__=["db","lm","admin","api","mail"]

db=SQLAlchemy()
lm=LoginManager()
admin=Admin(name="Vzer.Zhang",index_view=MyAdminIndexView(),base_template="admins/master.html",template_mode="bootstrap3")
api=Api()
mail=Mail()