#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json
import time
import psutil
import os

def main():
    fileRecord = open("hostInfo_temp.txt", "w")
    fileRecord.write("connect to vzer\n");
    fileRecord.close()
    while True:
        #获取主机信息
        cpu=(str)(psutil.cpu_percent(1))
        mem=(str)(psutil.virtual_memory().percent)
        #信息处理
        payload={"cpu":cpu,"mem":mem}
        # 设备URI
        #apiurl = 'http://58.210.99.102:8090/api/v1.0/weather'
        apiurl = 'http://192.168.80.246:8081/api/v1.0/weather'
        # 用户密码, 指定上传编码为JSON格式
        apiheaders = {'content-type': 'application/json'}
        #发送请求
        r = requests.post(apiurl,headers=apiheaders,data=json.dumps(payload))

        # 向控制台打印结果
        fileRecord = open("hostInfo_temp.txt", "a")
        strTime = time.strftime('%Y-%m-%d:%H-%M-%S',time.localtime(time.time()))
        fileRecord.writelines(strTime + "\n")
        strTemp = "%s" %payload + "\n"
        fileRecord.writelines(strTemp)
        fileRecord.writelines(str(r.status_code) + "\n")
        fileRecord.close()

        time.sleep(5*60)

if __name__ == '__main__':
    main()




