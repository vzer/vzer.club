#!/usr/bin/env python
#coding=utf-8
__author__ = 'vzer'
from flask_restful import Resource,reqparse,fields,marshal
from run import api
from datetime import datetime
from data_wrappers import Data_Wrappers


weathers= []
data=Data_Wrappers()
class Weather(Resource):
    weather_fields={
        "id":fields.Integer,
        "value":fields.Float,
        "datetime":fields.DateTime,
    }
    def get(self):
        weathers=data.get_temperature_all()
        return {"weathers":marshal(weathers,self.weather_fields)}

    def post(self):
        args=self.reqparse.parse_args()
        status=data.insert_temperature_all(value=args["value"])

        weather={
            "id":1,
            "value":args["value"],
            "datetime":datetime.now(),
        }
        weathers.append(weather)
        return {"weather":marshal(weather,self.weather_fields)}


    def __init__(self):
        self.reqparse=reqparse.RequestParser()
        self.reqparse.add_argument("value",type=float,required=True,help="value is must ",location="json")
        self.reqparse.add_argument("datetime",type=fields.datetime,location="json")
        super(Weather,self).__init__()

api.add_resource(Weather,"/api/v1.0/weather",endpoint="weather")
