# -- coding: utf-8 --
import json
import pymysql

def getConnection():
    return pymysql.connect(host='127.0.0.1', user='root', password='mysql',
                           db='mydb2', charset='utf8')

# datetime을 포함한 데이터를 json으로 바로 바꿀 수 있도록 추가한 함수
def user_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj

# name을 parameter로 받아 user 테이블에 추가
def createUser(name):
    conn = getConnection()
    curs = conn.cursor()
    ok = curs.execute("INSERT INTO user(name, create_datetime) VALUES (%s, now())", name)
    conn.commit()
    conn.close()

    return json.dumps({'rows': ok})

# user 테이블의 모든 user 읽기
def getAllUsers():
    conn = getConnection()

    curs = conn.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM user"
    curs.execute(sql)
   
    rows = curs.fetchall()
    conn.close()

    return json.dumps(rows, default=user_handler)