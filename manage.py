#!/usr/bin/env python
#coding=utf-8
__author__ = 'vzer'
from flask_script import Manager,Server
from application import create_app

server=Server(host="0.0.0.0",port=5000)
app=create_app()
manager=Manager(app)
manager.add_command("runserver", server)
if __name__ == '__main__':
    manager.run()