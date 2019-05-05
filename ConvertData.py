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
    create table if not exists convertData(
        commentId varchar(20) PRIMARY KEY NOT NULL,
        movieId varchar(20),
        userId varchar(20),
        nickName varchar(20),
        score integer,
        content varchar(20),
        cityName varchar(20),
        vipType integer,
        time datetime
    )
    ''')
    cursor.close()
    conn.commit()
    conn.close()

def insertItem(dbName, movieId,  item):
    conn = sqlite3.connect(dbName)
    conn.text_factory = str
    cursor = conn.cursor()
    sql = '''
    INSERT OR REPLACE INTO convertData values(?,?,?,?,?,?,?,?,?)
    '''
    values = (
        getValue(item, "id"), 
        movieId, 
        getValue(item, "userId"),
        getValue(item, "nickName"),
        getValue(item, "score"),
        getValue(item, "content"),
        getValue(item, "cityName"),
        getValue(item, "vipType"),
        getValue(item, "startTime"))
    cursor.execute(sql, values)
    cursor.close()
    conn.commit()
    conn.close()
    
def getValue(item, key):
    if item.has_key(key) :
        return item[key]
    else:
        return ""

def convert(dbName):
    conn = sqlite3.connect(dbName)
    conn.text_factory = str
    cursor = conn.cursor()
    cursor.execute("select * from comments")
    data = cursor.fetchall()
    for item in data:
        commentItem = json.loads(item[1])
        movieId = item[2]
        insertItem(dbName, movieId, commentItem)
    cursor.close()
    conn.commit()
    conn.close()


if __name__ == '__main__':
    dbName = "end.db"
    createDatabase(dbName)
    convert(dbName)