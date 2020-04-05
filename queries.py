import pandas as pd
import pymysql


def dataframe_creation(queries):
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='123qweasd',
                           database='tweets'
                           )
    c = conn.cursor()
    c.execute(queries)
    data = c.fetchall()
    col = [val[0] for val in c.description]
    conn.close()
    return pd.DataFrame(data=data, columns=col)


def db_clear(queries):
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='123qweasd',
                           database='tweets'
                           )
    c = conn.cursor()
    c.execute(queries)
    conn.commit()
    conn.close()


def table_insert(lis):
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='123qweasd',
                           database='tweets'
                           )
    c = conn.cursor()
    c.execute(
        """
        insert into tweets_stream
        (
        name,
        username,
        user_location,
        verified_status,
        followers,
        profile_pic,
        tweet,
        language,
        hashtags,
        retweet_count,
        favorite_count,
        created_at
        )
        values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, lis
    )
    conn.commit()
    conn.close()


table_creation_query = """
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

query = """
        select 
            created_at,
            case when verified_status = 1 then 'Verified Users' else 'Un-Verified Users' end as Status,
            count(*) as tweet_count
        from
            tweets_stream
        where 
            addtime(created_at,'7:00') > addtime(utc_timestamp(),'6:57')
        group by 
            1,2
        """

latest_tweet_query = """
        select
            *,
            addtime(created_at,'7:00') as local_time
        from
            tweets_stream
        where
            verified_status = 1
        order by 
            created_at desc
        limit 5
        """

today_hourly_query = """
        select
            case when verified_status = 1 then 'Verified Users' else 'Un-Verified Users' end as Status,
            case when hour(addtime(created_at,'7:00'))=24 then 0 else hour(addtime(created_at,'7:00')) end as hour,
            count(tweet) as tweet_count
        from
            tweets_stream
        where
            date(addtime(created_at,'7:00')) = date(addtime(utc_timestamp(),'7:00'))
        group by
            1,2
        order by 
            1,2
        """

user_count_query = """
        select 
            count(distinct username) as distinct_user,
            count(tweet) as total_count
        from 
            tweets_stream 
        where 
            date(addtime(created_at,'7:00')) = date(addtime(utc_timestamp(),'7:00'))
        """

delete_query = """
delete 
from 
    tweets_stream 
where 
    date(created_at) < date(adddate(utc_timestamp(),INTERVAL -2 DAY))
"""
