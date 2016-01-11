#!/usr/bin/env python
#coding=utf-8
__author__ = 'vzer'
from flask import render_template,flash,Module
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

leader=Module(__name__)

#blog 首页
@leader.route('/')
def index():
    return render_template("leader.html")
