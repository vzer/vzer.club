#!/usr/bin/env python
#coding=utf-8
__author__ = 'vzer'
import logging
import os
from logging.handlers import SMTPHandler,RotatingFileHandler
from vzerblog.extensions import db,lm,admin,api,mail
from flask import Flask,render_template,g
from vzerblog.develop_config import Develop_Config
from vzerblog import views
from leader import leader_views
from vzerblog.models import Data_Wrappers

DEFAULT_APP_NAME = "vzerblog"

DEFAULT_MODULES=(
    (leader_views.leader, "/"),
    (views.blog, "/blog")
)

data=Data_Wrappers()

def create_app(config=None,app_name=None,modules=None):
    if app_name is None:
        app_name=DEFAULT_APP_NAME

    if modules is None:
        modules=DEFAULT_MODULES

    app=Flask(app_name)
    configure_app(app,config)
    configure_logging(app)
    configure_errorhandlers(app)
    configure_before_handlers(app)
    configure_extensions(app)
    configure_modules(app,modules)

    return app

#config modules
def configure_modules(app,modules):

    for module, url_prefix in modules:
        app.register_module(module, url_prefix=url_prefix)

#config extension
def configure_extensions(app):
    db.init_app(app)
    lm.init_app(app)
    admin.init_app(app)
    api.init_app(app)
    mail.init_app(app)

#config config
def configure_app(app,config):
    app.config.from_object(Develop_Config)

    if config is not None:
        app.config.from_object(config)

    app.config.from_envvar("APP_CONFIG",silent=True)

#config log
def configure_logging(app):
    if app.debug or app.testing:
        return

    mail_handler=SMTPHandler(app.config["MAIL_SERVER"],
                  "584088967@qq.com",
                  app.config["ADMINS"],
                  "application error",
                  (
                      app.config["MAIL_USERNAME"],
                      app.config["MAIL_PASSWORD"],
                  ),)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

    formatter=logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    )

    debug_log=os.path.join(app.root_path,app.config["DEBUG_LOG"])

    debug_file_handler=RotatingFileHandler(
        debug_log,maxBytes=100000,backupCount=10
    )

    debug_file_handler.setLevel(logging.DEBUG)
    debug_file_handler.setFormatter(formatter)
    app.logger.addHandler(debug_file_handler)


    error_log=os.path.join(app.root_path,app.config["ERROR_LOG"])
    error_file_handler=RotatingFileHandler(
        error_log,maxBytes=100000,backupCount=10
    )

    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(formatter)
    app.logger.addHandler(error_file_handler)
#config error pages
def configure_errorhandlers(app):
    if app.testing:
        return

    @app.errorhandler(404)
    def page_not_found(error=None):
        return render_template("errors/404.html"),404

    @app.errorhandler(403)
    def forbidden():
        return render_template("errors/403.html"),403

    @app.errorhandler(500)
    def server_error():
        return  render_template("errors/500.html"),500

    @app.errorhandler(401)
    def unauthorized():
        return render_template("errors/401.html"),401

#config before handlers
def configure_before_handlers(app):
    if app.testing:
        return
    @app.before_request
    def before_request():
        g.MyBlogMenu=data.get_all_category()
        g.FriendLink=data.get_friendlink()
    @lm.user_loader
    def load_user(user_id):
        return data.get_user_byid(user_id=user_id)