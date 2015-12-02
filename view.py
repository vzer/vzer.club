#!/usr/bin/env python
#coding=utf-8
__author__ = 'vzer'
from flask import Flask,render_template,request,redirect,url_for,session,flash,g,abort
from werkzeug.security import generate_password_hash
from run import app,db,lm
import datetime
from flask_login import login_required,login_user,current_user,logout_user
from data_wrappers import Data_Wrappers
from form import LinksForm,LoginForm,RegeditForm

data=Data_Wrappers()

@app.errorhandler(404)
def notfound404(error):
    return render_template("404.html"),404

@app.before_request
def before_request():
    g.MyBlogMenu=data.get_all_category()
    g.FriendLink=data.get_friendlink()

@app.route('/')
def index():
    entry=data.get_all_entries()
    categorys=data.get_all_category()
    return render_template("index.html",entry=entry,categorys=categorys)

@app.route("/message/")
def message():
    return render_template("message.html")

@app.route("/entry/<int:id>")
def show_entry(id):
    entry=data.get_entry_byid(id=id)
    return render_template("show_entry.html",post=entry)

@app.route("/friendlink/")
def show_friendlink():
    friendlink=data.get_friendlink()
    return render_template("show_friendlink.html",friendlink=friendlink)

@app.route("/inputlink/",methods=["GET","POST"])
def inputlink():
    form=LinksForm()
    if form.validate_on_submit():
        webname=form.webname.data
        weburl=form.weburl.data
        webtip=form.webtip.data
        contactqq=form.contactqq.data
        status=data.insert_link(webname=webname,webtip=webtip,weburl=weburl,contact=contactqq)
        if status:
            flash("已经添加成功，请耐性等待回复吧。")
        else:
            flash("已经存在相同信息的URL信息了。")
    return render_template("input_link.html",form=form)

@app.route("/show_weather/")
def show_weather():
    (lables,cpu,mem)=data.get_temperature()
    return render_template("show_weather.html",lables=lables,cpu=cpu,mem=mem)

@app.route("/login/",methods=["GET","POST"])
def login():
    form=LoginForm()
    return  render_template("admin/login.html",form=form)

@app.route("/regedit/",methods=["GET","POST"])
def regedit():
    form=RegeditForm()
    return render_template("admin/regedit.html",form=form)

@app.route("/search/",methods=["GET","POST"])
def search():
    if request.method=="GET":
        entry=False
        return render_template("search.html",entry=entry)
    if request.method=="POST":
        value=request.form["search"]
        entry=data.search_entry(value=value)
        return render_template("search.html",entry=entry)
@app.route("/category/<int:id>")
def category(id=0):
    entry=data.get_entry_bycategory(id=id)
    categorys=data.get_all_category()
    return render_template("show_category.html",entry=entry,categorys=categorys)

@app.route("/tag/<int:id>")
def tag(id=0):
    entry=data.get_entry_bytag(id=id)
    categorys=data.get_all_category()
    return render_template("show_tag.html",entry=entry,categorys=categorys)