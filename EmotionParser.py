#!/usr/bin/python
#coding: utf-8
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
from snownlp import SnowNLP
import sys

reload(sys)
sys.setdefaultencoding( "utf-8" )

def emotionParser(name):
    conn = conn = sqlite3.connect("end.db")
    conn.text_factory = str
    cursor = conn.cursor()
    likeStr = "like \"%" + name + "%\""
    cursor.execute("select content from convertData where content " + likeStr)
    values = cursor.fetchall()
    sentimentslist = []
    for item in values:
        # print SnowNLP(item[0].decode("utf-8")).words
        sentimentslist.append(SnowNLP(item[0].decode("utf-8")).sentiments)
    plt.hist(sentimentslist, bins=np.arange(0, 1, 0.01), facecolor="#4F8CD6")  
    plt.xlabel("Sentiments Probability")                                       
    plt.ylabel("Quantity")                                                     
    plt.title("Analysis of Sentiments for " + name)                                        
    plt.show()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    name = raw_input("请输入名字:")
    emotionParser(name)