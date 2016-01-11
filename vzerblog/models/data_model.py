#!/usr/bin/env python
#coding=utf-8
__author__ = 'vzer'

from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from  vzerblog.extensions import db


#用户认证
class User(db.Model,UserMixin):
    __table_args__={"extend_existing":True,
                    "mysql_engine":"InnoDB",
                    "mysql_charset":"utf8"}
    __tablename__="user"
    id=db.Column(db.INTEGER,primary_key=True,autoincrement=True,unique=True)
    account=db.Column(db.String(50),unique=True)
    password=db.Column(db.String(100))
    email=db.Column(db.String(100))
    nickname=db.Column(db.String(50))
    isactive=db.Column(db.Boolean,default=False)
    isadmin=db.Column(db.Boolean,default=False)
    createtime=db.Column(db.DateTime,default=db.func.now())
    updatetime=db.Column(db.DateTime)
    logintime=db.Column(db.DateTime)

    def __init__(self,user_account=None,user_password=None,user_email=None,user_nickname=None,isactive=False,isadmin=False,updatetime=None):
        self.account=user_account
        self.set_password(password=str(user_password))
        self.email=user_email
        self.nickname=user_nickname
        self.isactive=isactive
        self.isadmin=isadmin
        self.updatetime=updatetime

    def set_password(self,password):
        self.password=generate_password_hash(password=password)

    def check_password(self,password):
        return check_password_hash(self.password,password=password)

    def set_logintime(self,logintime):
        self.logintime=logintime

    def get_logtime(self):
        return self.logintime

    def set_updatetime(self):
        self.updatetime=db.func.now()

    def get_updatetime(self):
        return self.updatetime

    def is_active(self):
        if self.isactive:
            return True
        else:
            return False

    def is_admin(self):
        if self.isadmin:
            return True
        else:
            return False


    def is_authenticated(self):
        return True


    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)


    def __repr__(self):
        return "<User '{:s}'> ".format(self.nick_name)

#类别模型
class Category(db.Model):
    __table_args__={"extend_existing":True,
                    "mysql_engine":"InnoDB",
                    "mysql_charset":"utf8"}
    __tablename__="category"
    id=db.Column(db.INTEGER,primary_key=True,autoincrement=True,unique=True)
    categoryname=db.Column(db.String(50))

    def __repr__(self):
        return "%s"%self.categoryname
#标签模型
class Tag(db.Model):
    __table_args__={"extend_existing":True,
                    "mysql_engine":"InnoDB",
                    "mysql_charset":"utf8"}
    __tablename__="tag"
    id=db.Column(db.INTEGER,primary_key=True,autoincrement=True,unique=True)
    name=db.Column(db.String(50))

    def __repr__(self):
        return "%s"%self.name

#tag,entry 关系表
tag_entry=db.Table('tags',
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                db.Column('entry_id', db.Integer, db.ForeignKey('entry.id')),
                extend_existing=True,
)

#文章模型
class Entry(db.Model):
    __table_args__={"extend_existing":True,
                    "mysql_engine":"InnoDB",
                    "mysql_charset":"utf8"}
    __tablename__="entry"
    id=db.Column(db.INTEGER,primary_key=True,autoincrement=True,unique=True)
    title=db.Column(db.String(150))
    fragment = db.Column(db.Text) #内容片段, 用于主页显示
    content = db.Column(db.Text)
    create_time = db.Column(db.DateTime, index=True, default=db.func.now())
    modified_time = db.Column(db.DateTime, default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    view_count = db.Column(db.Integer, default=0)

    category = db.relationship(Category, backref=db.backref('entry', lazy='dynamic'), lazy='select')
    tag=db.relationship(Tag,secondary=tag_entry,backref=db.backref('entries', lazy='dynamic'))

    def __repr__(self):
        return '<Entry %r>' % self.title

    def __unicode__(self):
        return self.title

# 友链
class Friend_link(db.Model):
    __table_args__={"extend_existing":True,
                    "mysql_engine":"InnoDB",
                    "mysql_charset":"utf8"}
    __tablename__="friendlink"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    tip=db.Column(db.String(300))
    link_url = db.Column(db.String(100),unique=True)
    contact=db.Column(db.String(100))
    display_index=db.Column(db.Boolean,default=False)
    isavaliable=db.Column(db.Boolean,default=False)

    def __repr__(self):
        return '<Friend link %r>' % self.name

    def __unicode__(self):
        return self.name

#喜欢
class Like(db.Model):
    __table_args__={"extend_existing":True,
                    "mysql_engine":"InnoDB",
                    "mysql_charset":"utf8"}
    __tablename__="like"
    id=db.Column(db.Integer,primary_key=True)
    like_count=db.Column(db.Integer)

#温度
class Temperature(db.Model):
    __table_args__={"extend_existing":True,
                    "mysql_engine":"InnoDB",
                    "mysql_charset":"utf8"}
    __tablename__="temperature"
    id=db.Column(db.INTEGER,primary_key=True,autoincrement=True)
    cpu=db.Column(db.Float)
    mem=db.Column(db.Float)
    datetime=db.Column(db.DateTime,default=db.func.now())

if __name__ == '__main__':
    db.create_all()
