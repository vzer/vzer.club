#!/usr/bin/env python
#coding=utf-8
__author__ = 'vzer'
from flask import render_template,request,flash,Module,current_app,session
from vzerblog.forms.form import LinksForm,LoginForm,RegeditForm
from vzerblog.models import Data_Wrappers
from vzerblog.email import input_link_mail
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
data=Data_Wrappers()

blog=Module(__name__)

#blog 首页
@blog.route('/')
@blog.route('/<int:page>/')
def index(page=1):
    pre_page=current_app.config.get("POST_PRE_PAGE")
    if page<1:
        page=1
    pagination=data.get_all_entries(page=page,per_page=pre_page)
    entry=pagination.items
    tags=data.get_tags()
    return render_template("index.html", entry=entry, tags=tags,pagination=pagination)

# 搜索页面
@blog.route("/search/",methods=["GET","POST"])
@blog.route("/search/<int:page>/",methods=["GET","POST"])
def search(page=1,value=None):
    if request.method=="GET":
        if page<1:
            page=1
        if session.has_key("searchkey"):
            value=session["searchkey"]
            print "search_key",value
            pre_page=current_app.config.get("POST_PRE_PAGE")
            pagination=data.search_entry(value=value,page=page,pre_page=pre_page)
            entry=pagination.items
            return render_template("search.html", entry=entry,pagination=pagination)
        else:
            entry=None
            return render_template("search.html",entry=entry)
    if request.method=="POST":
        pre_page=current_app.config.get("POST_PRE_PAGE")
        if page<1:
            page=1
        value=request.form["search"]
        session["searchkey"]=value
        pagination=data.search_entry(value=value,page=page,pre_page=pre_page)
        entry=pagination.items
        return render_template("search.html", entry=entry,pagination=pagination)

#分类页面
@blog.route("/category/<int:id>")
@blog.route("/category/<int:id>/<int:page>/")
def category(id=0,page=None):
    pre_page=current_app.config.get("POST_PRE_PAGE")
    if page<1:
            page=1
    pagination=data.get_entry_bycategory(id=id,page=page,pre_page=pre_page)
    entry=pagination.items
    tags=data.get_tags()
    return render_template("show_category.html", entry=entry,tags=tags,value=id,pagination=pagination)

#tag页面
@blog.route("/tag/<string:name>")
@blog.route("/tag/<string:name>/<int:page>/")
def tag(name=None,page=None):
    pre_page=current_app.config.get("POST_PRE_PAGE")
    if page<1:
            page=1
    pagination=data.get_entry_bytag(name=name,page=page,pre_page=pre_page)
    entry=pagination.items
    tags=data.get_tags()
    return render_template("show_tag.html", entry=entry, tags=tags,value=name,pagination=pagination)

#留言页面
@blog.route("/message/")
def message():
    return render_template("message.html")
#文章查看页面
@blog.route("/entry/<int:id>")
def show_entry(id):
    entry=data.get_entry_byid(id=id)
    return render_template("show_entry.html", post=entry)
#友情链接
@blog.route("/friendlink/")
def show_friendlink():
    friendlink=data.get_friendlink()
    return render_template("show_friendlink.html", friendlink=friendlink)
#提交友情链接
@blog.route("/inputlink/",methods=["GET","POST"])
def inputlink():
    form=LinksForm()
    if form.validate_on_submit():
        webname=form.webname.data
        weburl=form.weburl.data
        webtip=form.webtip.data
        contactqq=form.contactqq.data
        status=data.insert_link(webname=webname,webtip=webtip,weburl=weburl,contact=contactqq)
        if status:
            input_link_mail(contact=contactqq,webname=webname,weburl=weburl,webtip=webtip)
            flash("已经添加成功，请耐性等待回复吧。")
        else:
            flash("已经存在相同信息的URL信息了。")
    return render_template("input_link.html", form=form)
#查看天气
@blog.route("/show_weather/")
def show_weather():
    (lables,cpu,mem)=data.get_temperature()
    return render_template("show_weather.html", lables=lables, cpu=cpu, mem=mem)


