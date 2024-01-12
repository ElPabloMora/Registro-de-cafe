import pymysql


def connect_base():
    return pymysql.connect(host='localhost',user='root',passwd='password',db='registroCafe')