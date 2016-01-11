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

#登录
class LoginForm(Form):
    loginName=StringField("登录账户",validators=[DataRequired(message="ERROR！栏位不能为空！")])
    loginPassword=PasswordField("登录密码",validators=[DataRequired(message="ERROR！栏位不能为空！")])
    submit=SubmitField(label="点击登录")




#注册
class RegeditForm(Form):
    regeditName=StringField("登录账户",validators=[DataRequired(message="ERROR！栏位不能为空！")])
    nickName=StringField("真实姓名",validators=[DataRequired(message="ERROR！栏位不能为空！")])
    password=PasswordField("登录密码",validators=[DataRequired(message="ERROR！栏位不能为空！")])
    repeatpassword=PasswordField("登录密码",validators=[DataRequired(message="ERROR！栏位不能为空！"),EqualTo("password",message="两次密码不一致！")])
    email=StringField("联系邮箱",validators=[Email(message="邮件地址格式不正确！")])
    invitationCode=StringField("邀请码",validators=[DataRequired(message="ERROR！栏位不能为空！")])
    submit=SubmitField(label="点击注册")


