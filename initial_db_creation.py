import pymysql
import os
socket = os.path.join('/cloudsql', 'tweet-streamer-273219:asia-east1:tweet-streamer')

conn = pymysql.connect(
    unix_socket=socket,
    user='root',
    password='123qweasd',
    database='tweets'
)
c = conn.cursor()

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
