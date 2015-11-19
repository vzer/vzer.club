#!/usr/bin/env python
#coding=utf-8
__author__ = 'vzer'
from flask import Flask,render_template,request,redirect,url_for,session,flash,g,abort
from werkzeug.security import generate_password_hash
from run import app,db,lm
import datetime
from flask_login import login_required,login_user,current_user,logout_user
from data_wrappers import Data_Wrappers

data=Data_Wrappers()

@app.route('/')
def index():
    entry=data.get_all_entries()
    categorys=data.get_all_category()
    return render_template("index.html",entry=entry,categorys=categorys)

@app.route("/message")
def message():
    return render_template("message.html")