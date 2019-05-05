
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

# reload(sys)
# sys.setdefaultencoding( "utf-8" )

if __name__ == '__main__':
    conn = sqlite3.connect('end.db')
    conn.text_factory = str
    data = pd.read_sql("select * from convertData", conn)
    rateData = data.groupby(['score'])
    rateDataCount = rateData["time"].agg([ "count"])
    rateDataCount.reset_index(inplace=True)
    count = rateDataCount.shape[0] - 1
    attr = [rateDataCount["score"][count - i] for i in range(0, rateDataCount.shape[0])]    
    v1 = [rateDataCount["count"][count - i] for i in range(0, rateDataCount.shape[0])]
    bar = Bar("rate")
    bar.add("count",attr,v1,is_stack=True,xaxis_rotate=30,yaxix_min=4.2,
        xaxis_interval=0,is_splitline_show=True)
    bar.render("html/rate_count.html")