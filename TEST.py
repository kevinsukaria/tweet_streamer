import sqlalchemy

db = sqlalchemy.create_engine(
    sqlalchemy.engine.url.URL(
        drivername="mysql+pymysql",
        username='root',
        password='123qweasd',
        database='tweets',
        query={"unix_socket": "/cloudsql/{}".format('tweet-streamer-273219:asia-east1:tweet-streamer')},
    ), )

conn = db.connect()

conn.execute(
    """
    CREATE TABLE IF NOT EXISTS tweets_stream (
    name VARCHAR(255),
    username VARCHAR(255),
    user_location VARCHAR(255),
    verified_status BOOLEAN,
    followers INT,
    profile_pic VARCHAR(255),
    tweet VARCHAR(255),
    language VARCHAR(255),
    hashtags VARCHAR(255),
    retweet_count INT,
    favorite_count INT,
    created_at VARCHAR(255)

    )
    """
)

conn.execute(
    """
    CREATE DATABASE IF NOT EXISTS tes_database
    """
)