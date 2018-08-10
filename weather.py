# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
Created on Wed Aug 08 14:51:10 2018

@author: chenwa2x
"""
import itchat
import requests
import json
import time
import re
import datetime

class Weather(object):
    def __init__(self,city):
        self.city=city
        
    def get_weather(self):
        url = "http://wthrcdn.etouch.cn/weather_mini?citykey=101020100"
        res = requests.get(url)
        results = json.loads(res.content.decode("utf-8"), encoding="utf-8")
        return results
    
    def deal_info(self,dic):
        self.date = time.strftime("%Y年%m月", time.localtime()) + dic["date"].encode("utf-8")
        self.high = "最高温度： " + dic["high"].encode("utf-8")
        self.low = "最低温度： " + dic["low"].encode("utf-8")
        self.low = "最低温度： " + dic["low"].encode("utf-8")
        self.wind = "风向： " + dic["fengxiang"].encode("utf-8")
        self.power = re.findall("CDATA\[(.*)\]\]",dic["fengli"].encode("utf-8"))
        self.power = "风力： " + self.power[0]
        self.main = "天气： " + dic["type"].encode("utf-8")
        self.results = self.date + "\n"*2 + self.high + "\n" + self.low + "\n" + self.wind + "\n" + self.power + "\n" + self.main + "\n"
        return self.results


def send_info():
    c = Weather("shanghai")
    results = c.get_weather()
    today = results["data"]["forecast"][0]
    #tomorrow = results["data"]["forecast"][1]  
    #day_after_tomorrow = results["data"]["forecast"][3]
    tips = results["data"]["ganmao"]
    total = c.deal_info(today) + "\n" + tips.encode("utf-8") + "\n"
    print total.decode("utf-8")
    itchat.send(total.decode("utf-8"), "filehelper")

def time_send():
    flag = 0
    last_time = datetime.datetime(2018,8,10,16,06,0)
    while True:
        now = datetime.datetime.now()
        if  now > last_time + datetime.timedelta(hours=1) :  # 因为时间秒之后的小数部分不一定相等，要标记一个范围判断
            send_info()
            print("Sent message!")
            last_time = datetime.datetime.now()
            time.sleep(36000)    # 每次判断间隔1s，避免多次触发事件
            flag = 1
        else :
            if flag == 1 :
                last_time = last_time + datetime.timedelta(hours=1)
                flag = 0

if __name__ == "__main__":
    itchat.auto_login(True)
    time_send()
    
