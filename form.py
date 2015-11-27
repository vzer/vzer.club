#!/usr/bin/env python
#coding=utf-8
__author__ = 'vzer'
from flask_wtf import Form
from wtforms import StringField,PasswordField,BooleanField,SubmitField,TextAreaField
from wtforms.validators import DataRequired,Length,Email,EqualTo

#友情链接
class LinksForm(Form):
    webname=StringField("网站名称",validators=[DataRequired(message="栏位不能为空。")])
    weburl=StringField("网站地址",validators=[DataRequired(message="栏位不能为空。")])
    contactqq=StringField("联系方式",validators=[DataRequired(message="栏位不能为空。")])
    webtip=TextAreaField("网站介绍",validators=[DataRequired(message="栏位不能为空。")])
    submit=SubmitField(label="提交信息")