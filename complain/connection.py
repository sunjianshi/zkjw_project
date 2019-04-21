#!/user/bin/env python
# -*- coding: utf-8 -*-

import json
import cx_Oracle as oracle
from redis import Redis


res = Redis(host='127.0.0.1', port=6379, db=11)

def conns(dict_iterable = None):
    db = oracle.connect('bq_data','tiger','39.107.57.229:1521/orcl.lan')
    cursor = db.cursor()
    if dict_iterable:
        sql = "insert into CRAW_COMPLAIN_ONE (ID, TC_NUMBERS, BRAND, CAR_SERIES, CAR_TYPE, CAR_DESCRIBE, CAR_QUESTION, START_TIME, STATUS, SOURCE) values (COMPLAINT_SQE.NEXTVAL,:TC_NUMBERS, :BRAND, :CAR_SERIES, :CAR_TYPE, :CAR_DESCRIBE, :CAR_QUESTION, :START_TIME, :STATUS, :SOURCE)"
        cursor.executemany(sql, dict_iterable)
    db.commit()
    cursor.close()
    db.close()

def check_url(url):
    db = oracle.connect('bq_data', 'tiger', '39.107.57.229:1521/orcl.lan')
    cursor = db.cursor()
    sql = "select CAR_LINK from  CRAW_COMPLAIN_LINK where CAR_LINK = '%s'"%url
    print('sql',sql)
    cursor.execute(sql)
    data = cursor.fetchone()
    db.commit()
    cursor.close()
    db.close()
    if data:
        return data
    else:
        return None

def set_url(url):
    db = oracle.connect('bq_data', 'tiger', '39.107.57.229:1521/orcl.lan')
    cursor = db.cursor()
    if isinstance(url, list):
        sql = "insert into CRAW_COMPLAIN_LINK (ID, CAR_LINK) values (craw_complain_url.NEXTVAL,:CAR_LINK)"
        cursor.executemany(sql, url)
    else:
        sql = "insert into CRAW_COMPLAIN_LINK (ID, CAR_LINK) values (craw_complain_url.NEXTVAL,'%s')"%url
        cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()

def conn_recall(dict_iterable = None):
    db = oracle.connect('bq_data', 'tiger', '39.107.57.229:1521/orcl.lan')
    cursor = db.cursor()
    sql = "INSERT INTO CRAW_COMPLAIN_RECALL (ID, CAR_SERIES, CAR_TYPE, TITLE, CAR_CONTENT, START_TIME, STATUS, SOURCE, BRAND, CAR_LINK) VALUES (craw_complain_url.NEXTVAL, :CAR_SERIES, :CAR_TYPE, :TITLE, :CAR_CONTENT, :START_TIME, :STATUS, :SOURCE, :BRAND, :CAR_LINK)"
    cursor.executemany(sql, dict_iterable)
    db.commit()
    cursor.close()
    db.close()

def redis_set(url, num = 1):
    if isinstance(url,list):
        for i in url:
            res.set(i, num)
    else:
        res.set(url, num)

def redis_get(str):
    return res.get(str)


def redis_to_oracle():
    res = Redis(host='127.0.0.1', port=6379, db=11)
    urls = res.keys()
    print(urls)
    url_list = []
    for i in urls:
        url_dict = {}
        # check_url(i.decode())
        url_dict['car_link'] = i.decode()
        url_list.append(url_dict)
    # for url in url_list:
    #     urls = []
    #     print(url)
    #     urls.append(url)
    #     print(urls)
    #     check_url(urls)
    print(url_list)
    set_url(url_list)

# redis_to_oracle()