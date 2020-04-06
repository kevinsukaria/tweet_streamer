import datetime
import logging
import os
import sqlalchemy

# socket = os.path.join('/cloudsql', 'tweets-streamer:asia-east2:tweets-streamer')

db_user = os.environ.get("DB_USER")
db_pass = os.environ.get("DB_PASS")
db_name = os.environ.get("DB_NAME")
cloud_sql_connection_name = os.environ.get("CLOUD_SQL_CONNECTION_NAME")

db = sqlalchemy.create_engine(
    sqlalchemy.engine.url.URL(
        drivername="mysql+pymysql",
        username=db_user,
        password=db_pass,
        database=db_name,
        query={"unix_socket": "/cloudsql/{}".format(cloud_sql_connection_name)},
    ),)


# conn = pymysql.connect(
#     host = '35.220.176.195',
#     # unix_socket=socket,
#     user='root',
#     password='123qweasd',
#     database='tweets-streamer'
# )
# c = conn.cursor()
c = db.connect()
c.execute("""
    CREATE TABLE IF NOT EXISTS tweets_stream (
    name VARCHAR(255),
    username VARCHAR(255),
    user_location VARCHAR(255),
    verified_status VARCHAR(6),
    followers INT,
    profile_pic VARCHAR(255),
    tweet LONGTEXT,
    language VARCHAR(255),
    hashtags LONGTEXT,
    retweet_count INT,
    favorite_count INT,
    created_at DATETIME

    )
    """)
