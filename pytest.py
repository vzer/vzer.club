#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json
import time

def main():
    fileRecord = open("temperature_temp.txt", "w")
    fileRecord.write("connect to vzer\n");
    fileRecord.close()
    while True:
        # 打开文件
        file = open("/home/pi/wddatafile.txt")
        # 读取结果，并转换为浮点数
        payload = file.read()#已经是json 格式
        # 关闭文件
        file.close()

        # 设备URI
        apiurl = 'http://58.210.99.102:8090/api/v1.0/weather'
        #apiurl = 'http://192.168.80.246:8081/api/v1.0/weather'
        # 用户密码, 指定上传编码为JSON格式
        apiheaders = {'content-type': 'application/json'}
        #发送请求
        r = requests.post(apiurl,headers=apiheaders,data=payload)

        # 向控制台打印结果
        fileRecord = open("temperature_temp.txt", "a")
        strTime = time.strftime('%Y-%m-%d:%H-%M-%S',time.localtime(time.time()))
        fileRecord.writelines(strTime + "\n")
        strTemp = "%s" %payload + "\n"
        fileRecord.writelines(strTemp)
        fileRecord.writelines(str(r.status_code) + "\n")
        fileRecord.close()

        time.sleep(5*60)

if __name__ == '__main__':
    main()

