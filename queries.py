import _sqlite3
import pandas as pd



def dataframe_creation(queries):
    conn = _sqlite3.connect('tweets.db', timeout=15)
    c = conn.cursor()
    c.execute(queries)
    data = c.fetchall()
    col = [val[0] for val in c.description]
    conn.close()
    return pd.DataFrame(data=data, columns=col)

def db_clear(queries):
    conn = _sqlite3.connect('tweets.db', timeout=15)
    c = conn.cursor()
    c.execute(queries)
    conn.commit()
    conn.close()

query = """
        select 
            created_at,
            count(*) as tweet_count
        from
            tweets_stream
        where 
            date(created_at,'+7 hour') = date('now','+7 hour')
        group by 
            1
        """

latest_tweet_query = """
        select
            *,
            datetime(created_at,'+7 hour') as local_time
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
            case when strftime('%H',datetime(created_at,'+7 hour'))=24 then 0 else strftime('%H',datetime(created_at,'+7 hour')) end as hour,
            count(tweet) as tweet_count
        from
            tweets_stream
        where
            date(created_at,'+7 hour') = date('now','+7 hour')
        group by
            1
        order by 
            1
        """

user_count_query = """
        select 
            count(distinct username) as distinct_user 
        from 
            tweets_stream 
        where 
            date(created_at,'+7 hour') = date('now','+7 hour')
        """

delete_query = """
delete 
from 
    tweets_stream 
where 
    date(created_at,'+7 hour') < date('now','+7 hour','-3 day')
"""
