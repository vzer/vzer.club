#!/usr/bin/env python
#coding=utf-8
__author__ = 'vzer'
from data_model import User, Tag, Entry, Category, Friend_link, tag_entry
from run import db

class Data_Wrappers(object):
    def get_all_entries(self):
        return Entry.query.all()

    def get_all_category(self):
        return Category.query.all()

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