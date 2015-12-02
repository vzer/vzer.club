#!/usr/bin/env python
#coding=utf-8
__author__ = 'vzer'
from flask_restful import Resource,reqparse,fields,marshal
from run import api
from datetime import datetime
from data_wrappers import Data_Wrappers


data=Data_Wrappers()
class Weather(Resource):
    info_fields={
        "id":fields.Integer,
        "cpu":fields.Float,
        "mem":fields.Float,
        "datetime":fields.DateTime,
    }
    def get(self):
        get_infos=data.get_temperature_all()
        return {"infos":marshal(get_infos,self.info_fields)}

    def post(self):
        args=self.reqparse.parse_args()
        status=data.insert_temperature_all(cpu=args["cpu"],mem=args["mem"])
        if status:
            info={
                "id":1,
                "cpu":args["cpu"],
                "mem":args["mem"],
                "datetime":datetime.now(),
            }
            return {"weather":marshal(info,self.info_fields)}
        else:
            return "post fail!"


    def __init__(self):
        self.reqparse=reqparse.RequestParser()
        self.reqparse.add_argument("cpu",type=float,required=True,help="cpu is must ",location="json")
        self.reqparse.add_argument("mem",type=float,required=True,help="mem is must ",location="json")
        self.reqparse.add_argument("datetime",type=fields.datetime,location="json")
        super(Weather,self).__init__()

api.add_resource(Weather,"/api/v1.0/weather",endpoint="weather")
