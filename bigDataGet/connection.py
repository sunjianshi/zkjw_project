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

def conn(sql):
    db = oracle.connect('bq_data', 'tiger', '39.107.57.229:1521/orcl.lan')
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()

def redis_set(url, num = 1):
    if isinstance(url,list):
        for i in url:
            res.set(i,num)
    else:
        res.set(url, num)

def redis_get(str):
    return res.get(str)