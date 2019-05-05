#!/usr/bin/python
#coding: utf-8
import requests
import datetime,time
import random
import json
import io
import sqlite3
import os, subprocess
import sys

def createDatabase(dbName):
    conn = sqlite3.connect(dbName)
    conn.text_factory=str
    cursor = conn.cursor()
    cursor.execute('''
    create table if not exists comments(
        commentId varchar(20) PRIMARY KEY NOT NULL,
        originalData TEXT,
        movieId varchar(20)
    )
    ''')
    cursor.close()
    conn.commit()
    conn.close()

def saveMoveInfoToFile(dbName, movieId, startTime, endTime): 
    while startTime > endTime :
        try: 
            url = "http://m.maoyan.com/mmdb/comments/movie/" + movieId + ".json?_v_=yes&offset=20&startTime=" + startTime.replace(" ", "%20")
            resultTime = saveMoveInfoToDatabase(dbName, movieId, url)
            tempTime = datetime.datetime.strptime(resultTime, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(seconds=-1)
            print "resultTime:" + resultTime +  "  t:" + str(tempTime)
            startTime = datetime.datetime.strftime(tempTime, "%Y-%m-%d %H:%M:%S")
        except Exception as e:
            print e
            time.sleep(5)
        else:
            time.sleep(1)

def saveMoveInfoToDatabase(dbName, movieId, url):
    print(url)
    html = getMoveinfo(url)
    items = parseMovieInfo(html)
    firstTime = ""
    count = 0
    for item in items: 
        firstTime = item['date']
        saveItem(dbName, movieId, item['id'], item['content'])
        count += 1
    return (firstTime)

def saveItem(dbName, moveId, id, originalData) :
    conn = sqlite3.connect(dbName)
    conn.text_factory=str
    cursor = conn.cursor()
    ins="INSERT OR REPLACE INTO comments values (?,?,?)"
    v = (id, originalData, moveId)
    cursor.execute(ins,v)
    cursor.close()
    conn.commit()
    conn.close()

def getMoveinfo(url):
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Mobile Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Cookie": "_lxsdk_cuid=16a4fc8324fc8-057564276922b5-35677607-232800-16a4fc83250c8; __mta=150912649.1556205618848.1556205618848.1556205618848.1; uuid_n_v=v1; iuuid=CF8755C0676D11E9A7D583E9F6D6E054E933915DE3554EE39B26E9FD516C4AC0; webp=true; ci=1%2C%E5%8C%97%E4%BA%AC; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk=A205B510676D11E9B5F83B51598F3073EAB7B5EC28694B7E8123505A55B1228E; _lxsdk_s=16a551544d6-cda-119-4ea%7C%7C35"
    }
    response = session.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    return None


def parseMovieInfo(html):
    data = json.loads(html)['cmts']
    for item in data:
        yield{
            'movieId':getValue(item, 'movieId'),
            'id':getValue(item, 'id'),
            'content':json.dumps(item),
            'date':getValue(item, 'startTime')
            }

def getValue(item, key):
    if item.has_key(key) :
        return item[key]
    else:
        return ""

if __name__ == '__main__':
    print("Welcome to Maoyan comments world!!")
    dbName = raw_input("Please Input the DB Name:")
    createDatabase(dbName)
    movieId = raw_input("Please Input the Movie ID:")
    saveMoveInfoToFile(dbName, movieId, "2019-04-25 21:59:44", "2018-04-25 22:00:00")
