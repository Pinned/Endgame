#!/usr/bin/python
#coding: utf-8
from wordcloud import WordCloud,STOPWORDS
import pandas as pd 
import jieba
import sqlite3
import matplotlib.pyplot as plt 
#import seaborn as sns
from pyecharts import Geo,Style,Line,Bar,Overlap,Map
import io
import requests
import time
import random
import json
import sys

reload(sys)
sys.setdefaultencoding( "utf-8" )

def getCommentCount(names):
    conn = conn = sqlite3.connect("end.db")
    conn.text_factory = str
    cursor = conn.cursor()
    likeStr = ""
    for i in range(0, len(names)):
        print names[i]
        likeStr = likeStr +  "content like \"%" + names[i] + "%\" "
        if i + 1 < len(names):
            likeStr = likeStr + " or "
    cursor.execute("select COUNT(content) from convertData where " + likeStr)
    values = cursor.fetchall()
    return values[0][0]

def getAlias(alias, name):
    if alias.has_key(name):
        return alias[name]
    else:
        return [name]

if __name__ == '__main__':
    attr = ["灭霸","美国队长",
         "钢铁侠", "浩克", "奇异博士",  "蜘蛛侠", "索尔" ,"黑寡妇", 
         "鹰眼", "惊奇队长", "幻视",
         "猩红女巫","蚁人", "古一法师", "洛基"]

    alias = {
        "灭霸": ["灭霸", "Thanos"],
        "美国队长": ["美国队长", "美队"],
        "浩克": ["浩克", "绿巨人", "班纳", "HULK"],
        "奇异博士": ["奇异博士", "医生"],
        "钢铁侠": ["钢铁侠", "stark", "斯塔克", "托尼", "史塔克"],
        "蜘蛛侠": ["蜘蛛侠","蜘蛛","彼得", "荷兰弟"],
        "索尔":["索尔", "雷神", "托尔"],
        "黑寡妇": ["黑寡妇", "寡姐"],
        "鹰眼":["鹰眼","克林顿","巴顿","克林特"],
        "惊奇队长":["惊奇队长","卡罗尔", "惊奇"],
        "星云":["星云"],
        "猩红女巫": ["猩红女巫", "绯红女巫", "旺达"],
        "蚁人":["蚁人", "蚁侠", "Ant", "AntMan"],
        "古一法师": ["古一", "古一法师", "法师"],
        "洛基": ["洛基", "抖森"]
    }
    v1 = [getCommentCount(getAlias(alias, attr[i])) for i in range(0, len(attr))]
    bar = Bar("Hiro")
    bar.add("count",attr,v1,is_stack=True,xaxis_rotate=30,yaxix_min=4.2,
        xaxis_interval=0,is_splitline_show=True)
    bar.render("html/hiro_count.html")
    