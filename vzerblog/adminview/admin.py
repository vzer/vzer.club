#!/usr/bin/env python
#coding=utf-8
__author__ = 'vzer'

from flask_admin import expose,AdminIndexView
from vzerblog.forms.form import LoginForm,RegeditForm
from flask import redirect,url_for,render_template,flash,request,current_app
from flask_login import login_user,current_user,logout_user



class MyAdminIndexView(AdminIndexView):
    def __init__(self):
        super(MyAdminIndexView,self).__init__(name="首页",url="/vzeradmin")

    @expose("/")
    def index(self):
        if not current_user.is_authenticated():
            return redirect(url_for("admin.login"))
        return self.render("admins/index.html")

    @expose("/login/",methods=["GET","POST"])
    def login(self):
        form=LoginForm(request.form)
        if current_user.is_authenticated():
            return redirect(url_for("admin.index"))
        if form.validate_on_submit():
            username=form.loginName.data
            password=form.loginPassword.data
            from vzerblog.models import Data_Wrappers
            data=Data_Wrappers()
            user=data.get_user_byname(username=username)
            if user is not None and user.check_password(password=password):
                if user.is_active():
                    login_user(user)
                    flash("hi,%s 您已经登录成功。"%current_user.nickname)
                    next=request.args.get("next")
                    return  redirect(next or url_for("admin.index"))
                else:
                    flash("账户未激活，请联系管理员。")
                    return self.render("admins/login.html", form=form)
            else:
                flash("用户名或密码出错啦。")
        return self.render("admins/login.html", form=form)


    @expose('/logout/')
    def logout(self):
        logout_user()
        return redirect(url_for('admin.login'))

    @expose("/register",methods=["GET","POST"])
    def register(self):
        form=RegeditForm()
        if form.validate_on_submit():
            account=form.regeditName.data
            nickname=form.nickName.data
            password=form.password.data
            email=form.email.data
            registercode=form.invitationCode.data
            if registercode!= current_app.config.get("REGISTERCODE"):
                flash("邀请码不正确啦，请联系站主吧。")
                return self.render("admins/regedit.html", form=form)
            else:
                from vzerblog.models import Data_Wrappers
                data=Data_Wrappers()
                flag=data.insert_user(account=account,nickname=nickname,email=email,password=password)
                if flag:
                    flash("已经注册成功啦，耐心等待审核把。")
                    return self.render("admins/regedit.html", form=form)
                else:
                    flash("失败啦，请过会再试把。")
                    return self.render("admins/regedit.html", form=form)
        return self.render("admins/regedit.html", form=form)


