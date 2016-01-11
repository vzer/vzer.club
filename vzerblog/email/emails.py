#!/usr/bin/env python
#coding=utf-8
__author__ = 'vzer'

from flask import render_template,current_app
from flask_mail import Message
from vzerblog.extensions import mail
from threading import Thread


def async(func):
    def wrapper(*args,**kwargs):
        thr=Thread(target=func,args=args,kwargs=kwargs)
        thr.start()
    return wrapper

@async
def send_async_mail(msg):
    from manage import app
    with app.app_context():
        mail.send(msg)


def send_mail(subject,sender,recipients,html_body):
    msg=Message(subject,recipients=recipients,sender=sender)
    msg.html=html_body
    send_async_mail(msg)
    #thr = Thread(target = send_async_mail, args = [msg])
    #thr.start()


def input_link_mail(contact,webname,weburl,webtip):
    send_mail(subject="[vzer.zhang]:友情链接提醒",sender=current_app.config.get("DEFAULT_MAIL_SENDER"),\
              recipients=current_app.config.get("ADMINS"),html_body=render_template("mail/email_inputlink.html",contact=contact,webname=webname,weburl=weburl,webtip=webtip))
