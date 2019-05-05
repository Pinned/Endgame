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



def getName(name,jsonObj):
    try:
        realNam = jsonObj[name]
        return realNam
    except:
        return ""

def getRealName(name, jsonObj):    
    for item in jsonObj:
        if (str(item)).startswith(name) :
            return jsonObj[item]
    return name
    
def realKeys(name):
    return name.replace(u"省", "").replace(u"市", "").replace(u"回族自治区", "").replace(u"维吾尔自治区", "").replace(u"壮族自治区", "").replace(u"自治区", "")

if __name__ == '__main__':
    conn = sqlite3.connect('end.db')
    conn.text_factory = str
    data = pd.read_sql("select * from convertData", conn)
    city = data.groupby(['cityName'])
    city_com = city['score'].agg(['mean','count'])
    city_com.reset_index(inplace=True)
    fo = open("citys.json",'r')
    citys_info = fo.readlines()
    citysJson = json.loads(str(citys_info[0]))
    print city_com
    data_map_all = [(getRealName(city_com['cityName'][i], citysJson),city_com['count'][i]) for i in range(0,city_com.shape[0])]
    data_map_list = {}
    for item in data_map_all:
        if data_map_list.has_key(item[0]):
            value = data_map_list[item[0]]
            value += item[1]
            data_map_list[item[0]] = value
        else:
            data_map_list[item[0]] = item[1]
    data_map = [(realKeys(key), data_map_list[key] ) for key in data_map_list.keys()]
    geo = Map("城市评论数", width= 1200, height = 800, title_pos="center")
    while True:
        try:
            attr,val = geo.cast(data_map)
            geo.add("",attr,val,visual_range=[0,6000],
                    visual_text_color="#fff",
                    symbol_size=5,
                    is_visualmap=True,
                    maptype=u'china',
                    is_map_symbol_show=False,
                    is_label_show=True,
                    is_roam=False, 
#                    visual_split_number=4
                    )
                    
        except ValueError as e:
            e = e.message.split("No coordinate is specified for ")[1]
            data_map = filter(lambda item: item[0] != e, data_map)
        else :
            break
    geo.render('OnlyMap.html')
    