#!/usr/bin/python
#coding: utf-8
from wordcloud import WordCloud,STOPWORDS
import pandas as pd 
from PIL import Image
import numpy as np
import jieba
import matplotlib.pyplot as plt 
#import seaborn as sns
from pyecharts import Geo,Style,Line,Bar,Overlap,Map
import io
from os import path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import sqlite3

if __name__ == '__main__':
    conn = sqlite3.connect('end.db')
    conn.text_factory = str
    data = pd.read_sql("select * from convertData", conn)
    jieba.add_word("钢铁侠", freq = 20000, tag = None)
    jieba.add_word("灭霸", freq = 20000, tag = None)
    jieba.add_word("复仇者联盟", freq = 20000, tag = None)
    jieba.add_word("美国队长", freq = 20000, tag = None)
    comment = jieba.cut(str(data['content']),cut_all=False)
    wl_space_split = " ".join(comment)
    backgroudImage = np.array(Image.open(r"/Users/zhaocheng/Downloads/qipashuo.jpeg"))
    stopword = STOPWORDS.copy()
    stopword.add(u"电影")
    stopword.add(u"没有")
    stopword.add(u"什么")
    stopword.add(u"漫威")
    stopword.add(u"还有")
    wc = WordCloud(width=1920,height=1080,background_color='white',
        mask=backgroudImage,
        font_path="/Users/zhaocheng/Documents/Deng.ttf",
        stopwords=stopword,max_font_size=400,
        random_state=50)
    wc.generate_from_text(wl_space_split)
    plt.imshow(wc)
    plt.axis("off")
    wc.to_file('unknow_word_cloud.png')