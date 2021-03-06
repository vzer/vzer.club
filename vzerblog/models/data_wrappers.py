#!/usr/bin/env python
#coding=utf-8
__author__ = 'vzer'
from sqlalchemy import or_
from data_model import Tag, Entry, Category, Friend_link, tag_entry,Temperature,User
from vzerblog.extensions import db

class Data_Wrappers(object):
    #获取所有的文章（添加分页）
    def get_all_entries(self,page,per_page):
        pages=Entry.query.order_by(Entry.create_time.desc()).paginate(page,per_page)
        return pages
    #获取所有分类
    def get_all_category(self):
        return Category.query.order_by(Category.id.desc()).all()
    #根据id获取文章
    def get_entry_byid(self,id):
        return Entry.query.filter(Entry.id==id).first()
    #根据类别获取文章
    def get_entry_bycategory(self,id,page,pre_page):
        pages=Entry.query.filter(Entry.category_id==id).paginate(page,pre_page)
        return pages
    #根据tag获取文章
    def get_entry_bytag(self,name,page,pre_page):
        pages=Entry.query.filter(Entry.tag.any(name=name)).paginate(page,pre_page)
        return pages
     #根据条件搜索文章字段
    def search_entry(self,value,page,pre_page):
        pages=Entry.query.filter(or_(Entry.title.like("%%%s%%"%value),Entry.content.like("%%%s%%"%value))).paginate(page,pre_page)
        return pages
    #获取tag
    def get_tags(self):
        tags=Tag.query.all()
        return tags

    #获取首页显示，审核过的友情链接
    def get_friendlink(self):
        return Friend_link.query.filter(Friend_link.display_index==True,Friend_link.isavaliable==True).all()
    #获取所有审核过的友情链接
    def get_friendlink_all(self):
        return Friend_link.query.filter(Friend_link.isavaliable==True).all()
    #检查友情链接的url是否已经存在
    def check_friendlink(self,url):
        link=Friend_link.query.filter(Friend_link.link_url==url).all()
        if link:
            return True
        else:
            return False
    #插入友情链接
    def insert_link(self,webname,webtip,weburl,contact):
        link=Friend_link(name=webname,tip=webtip,link_url=weburl,contact=contact)
        flag=self.check_friendlink(weburl)
        if not flag:
            db.session.add(link)
            try:
                db.session.commit()
                return True
            except Exception:
                db.session.rollback()
        else:
            return False

    #插入文章
    def create_entry(self, title, content, tag, category):
        ent = Entry(title=title, content=content, category_id=category, create_time=db.func.now())
        #查找tag是否存在,并加入tags，如果不存在则创建tag
        tag_list = tag_entry.split()
        for tag_name in tag_list:
            t = db.session.query(Tag).filter(Tag.name == tag_name).first()
            if not t:
                t = Tag(tag_name)
            ent.tag.append(t)

        db.session.add(ent)
        db.comit()
        return ent
    #获取最近1小时内的cpu，内存利用率
    def get_temperature(self):
        labels=[]
        cpu=[]
        mem=[]
        tem=Temperature.query.filter(db.text("datetime>date_add(NOW(),INTERVAL -1 HOUR)")).all()
        for kk in tem:
            labels.append(str(kk.datetime))
            cpu.append(kk.cpu)
            mem.append(kk.mem)
        return (labels,cpu,mem)
    #获取所有的cpu，内存利用率记录
    def get_temperature_all(self):
        return Temperature.query.all()
    #插入cpu，内存利用率记录
    def insert_temperature_all(self,cpu=None,mem=None):
        link=Temperature(cpu=cpu,mem=mem)
        db.session.add(link)
        try:
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False

    #根据id获取用户
    def get_user_byid(self,user_id):
        return User.query.get(user_id)
    #根据用户名获取用户
    def get_user_byname(self,username):
        return User.query.filter(User.account==username).first()
    #检查用户是否存在
    def check_user(self,account):
        user=User.query.filter(User.account==account).all()
        if user:
            return True
        else:
            return False
    #添加用户
    def insert_user(self,account=None,nickname=None,email=None,password=None):
        user=User(user_account=account,user_password=password,user_email=email,user_nickname=nickname)
        flag=self.check_user(account)
        if not flag:
            db.session.add(user)
            try:
               db.session.commit()
               return True
            except Exception:
                db.session.rollback()
        else:
            return False

