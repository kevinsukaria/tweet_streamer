import pymysql

conn = pymysql.connect(host='localhost',
                     user='root',
                     password='123qweasd')

c = conn.cursor()
c.execute("create database if not exists tes_database")
conn.commit()