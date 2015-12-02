#!/usr/bin/env python
#coding=utf-8
__author__ = 'vzer'

from flask import Flask,url_for,request,redirect,g,flash
from flask.ext.login import current_user,login_user,logout_user
from flask_admin import Admin,expose,AdminIndexView
from flask_admin.contrib.sqla import ModelView
from run import app,db
from data_model import User,Category,Tag,Like,Entry,Friend_link
from wtforms.validators import required,Email
from wtforms import fields, widgets
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

#用户管理
class UserAdmin(ModelView):
    can_view_details = True
    create_modal = True
    edit_modal = True
    column_searchable_list = ["account","nickname","email"]
    column_filters = ["isactive","isadmin"]
    column_exclude_list = ["password"]
    column_details_exclude_list =["password"]
    form_excluded_columns = ["createtime","updatetime","logintime"]
    column_labels = dict(account="登录账户",email="电子邮箱",nickname="用户姓名",isadmin="管理",isactive="状态",createtime="创建日期",updatetime="修改时间",password="用户密码",logintime="登录时间")
    form_args = {
        "account":{
            "label":"登录账户",
            "validators":[required()]
        },
        "email":{
            "label":"电子邮箱",
            "validators":[required(),Email()]
        },
        "nickname":{
            "label":"用户名称",
            "validators":[required()]
        },
        "isactive":{
            "label":"是否激活",
        },
        "isadmin":{
            "label":"是否admin",
        },
        "createtime":{
            "label":"创建时间",
            "validators":[required()]
        },
        "password":{
            "label":"用户密码",
            "validators":[required()]
        },
        "updatetime":{
            "label":"更新时间",
            "validators":[required()]
        },
        "logintime":{
            "label":"登录时间",
            "validators":[required()]
        },
    }
    def __init__(self,session):
        super(UserAdmin,self).__init__(User,db.session,endpoint="user_view",name="用户管理")
    '''
    def is_accessible(self):
        return current_user.is_authenticated()

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("login",next=request.url))
    '''
    def create_model(self, form):
        try:
            model=self.model()
            form.populate_obj(model)
            model.set_password(model.password)
            self.session.add(model)
            self._on_model_change(form, model, True)
            self.session.commit()
        except Exception as ex:
            if not self.handle_view_exception(ex):
                flash('Failed to create record. %(error)s', error=str(ex))
            self.session.rollback()
            return False
        else:
            self.after_model_change(form, model, True)
        return model

    def update_model(self, form, model):
        try:
            form.populate_obj(model)
            if not("pbkdf2:sha1" in model.password):
                model.set_password(model.password)
            model.set_updatetime()
            self._on_model_change(form, model, False)
            self.session.commit()
        except Exception as ex:
            if not self.handle_view_exception(ex):
                flash('Failed to update record. %(error)s', error=str(ex))

            self.session.rollback()

            return False
        else:
            self.after_model_change(form, model, False)

        return True
#类别管理
class CategotyAdmin(ModelView):
    can_view_details = True
    create_modal = True
    edit_modal = True
    column_searchable_list = ["categoryname"]
    column_labels = dict(categoryname="类别名称")
    form_excluded_columns = ["entry"]
    form_args = {
        "categoryname":{
            "label":"类别名称",
            "validators":[required()]
        },
    }
    def __init__(self,session):
        super(CategotyAdmin,self).__init__(Category,db.session,endpoint="category_view",name="类别管理")

#标签管理
class TagAdmin(ModelView):
    can_view_details = True
    create_modal = True
    edit_modal = True
    column_searchable_list = ["name"]
    column_labels = dict(name="标签名")
    form_excluded_columns = ["entries"]

    form_args = {
        "name":{
            "label":"标签名",
            "validators":[required()]
        },
    }
    def __init__(self,session):
        super(TagAdmin,self).__init__(Tag,db.session,endpoint="tag_view",name="标签管理")

# Define wtforms widget and field
class CKTextAreaWidget(widgets.TextArea):

    def __call__(self, field, **kwargs):
        c=kwargs.pop("class","") or kwargs.pop("class_","")
        kwargs["class"]="%s %s"%(c,"ckeditor")
        kwargs.setdefault("rows","40")
        kwargs.setdefault("cols","80")
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(fields.TextField):
    widget = CKTextAreaWidget()

class EntryAdmin(ModelView):
    can_view_details = True
    column_searchable_list = ["title","category_id"]
    column_filters = ["category_id","tag.name"]
    column_exclude_list = ["content","fragment"]
    column_labels = dict(title="文章标题",fragment="内容简要",content="正文",create_time="创建时间",modified_time="修改时间",user_id="创建者",category_id="类别",tag="Tag",view_count="浏览次数")

    form_overrides = dict(content=CKTextAreaField)
    create_template = 'admin/create.html'
    edit_template = 'admin/edit.html'
    def __init__(self, session):
        super(EntryAdmin, self).__init__(Entry, db.session,endpoint="entry_view",name="文章管理")
    '''
    def is_accessible(self):
        return current_user.is_authenticated()
    '''

#友情链接管理
class Friend_Links(ModelView):
    can_view_details = True
    create_template = 'admin/create.html'
    edit_template = 'admin/edit.html'
    form_overrides = dict(tip=CKTextAreaField)
    def __init__(self,session):
        super(Friend_Links,self).__init__(Friend_link,db.session,endpoint="link_view",name="友情链接")


class MyAdminIndexView(AdminIndexView):
    @expose("/")
    def index(self):
        #if not current_user.is_authenticated():
            #return redirect(url_for("model_view_user.index_view"))
        return super(MyAdminIndexView,self).index()


    @expose('/logout/')
    def logout_view(self):
        logout_user()
        return redirect(url_for('index'))

    def __init__(self):
        super(MyAdminIndexView,self).__init__(name="首页",url="/vzeradmin")

admin=Admin(name="Vzer.Zhang",index_view=MyAdminIndexView(),base_template="/admin/master.html",template_mode="bootstrap3")
admin.add_view(UserAdmin(db.session()))
admin.add_view(CategotyAdmin(db.session()))
admin.add_view(TagAdmin(db.session()))
admin.add_view(EntryAdmin(db.session()))
admin.add_view(Friend_Links(db.session()))
admin.init_app(app)