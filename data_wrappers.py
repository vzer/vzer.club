#!/usr/bin/env python
#coding=utf-8
__author__ = 'vzer'
from data_model import Tag, Entry, Category, Friend_link, tag_entry,Temperature
from run import db

class Data_Wrappers(object):
    def get_all_entries(self):
        return Entry.query.all()

    def get_all_category(self):
        return Category.query.all()

    def get_entry_byid(self,id):
        return Entry.query.filter(Entry.id==id).first()

    def get_blogmenu(self):
        return Category.query.all()

    def get_friendlink(self):
        return Friend_link.query.filter(Friend_link.display_index==True,Friend_link.isavaliable==True).all()

    def get_friendlink_all(self):
        return Friend_link.query.filter(Friend_link.isavaliable==True).all()

    def check_friendlink(self,url):
        link=Friend_link.query.filter(Friend_link.link_url==url).all()
        if link:
            return True
        else:
            return False

    def get_temperature_all(self):
        return Temperature.query.all()

    def insert_temperature_all(self,value):
        link=Temperature(value=value)
        db.session.add(link)
        try:
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False


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


    #weather
    def get_temperature(self):
        labels=[]
        data=[]
        tem=Temperature.query.filter(db.text("datetime>date_add(NOW(),INTERVAL -1 HOUR)")).all()
        for kk in tem:
            labels.append(str(kk.datetime))
            data.append(kk.value)
        print labels
        return (labels,data)
