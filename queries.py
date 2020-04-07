import pandas as pd
import pymysql
import sqlalchemy

socket = '/cloudsql/tweets-streamer:asia-east2:tweets-streamer'

def dataframe_creation(queries):
    db = sqlalchemy.create_engine(
        # Equivalent URL:
        # mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=/cloudsql/<cloud_sql_instance_name>
        sqlalchemy.engine.url.URL(
            drivername="mysql+pymysql",
            username='root',
            password='123qweasd',
            database='tweets',
            query={"unix_socket": "/cloudsql/tweets-streamer:asia-east2:tweets-streamer"},
        ),)
    c = db.connect()
    c.execute(queries)
    data = c.fetchall()
    c.close()
    col = [val[0] for val in c.description]
    return pd.DataFrame(data=data, columns=col)


def db_clear(queries):
    db = sqlalchemy.create_engine(
        # Equivalent URL:
        # mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=/cloudsql/<cloud_sql_instance_name>
        sqlalchemy.engine.url.URL(
            drivername="mysql+pymysql",
            username='root',
            password='123qweasd',
            database='tweets',
            query={"unix_socket": "/cloudsql/tweets-streamer:asia-east2:tweets-streamer"},
        ), )
    c = db.connect()
    c.execute(queries)
    c.close()


def table_insert(lis):
    db = sqlalchemy.create_engine(
        # Equivalent URL:
        # mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=/cloudsql/<cloud_sql_instance_name>
        sqlalchemy.engine.url.URL(
            drivername="mysql+pymysql",
            username='root',
            password='123qweasd',
            database='tweets',
            query={"unix_socket": "/cloudsql/tweets-streamer:asia-east2:tweets-streamer"},
        ), )
    c = db.connect()
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
    c.commit()
    c.close()

query = """
        select 
            created_at,
            case when verified_status = 1 then 'Verified Users' else 'Un-Verified Users' end as Status,
            count(*) as tweet_count
        from
            tweets_stream
        where 
            addtime(created_at,'7:00') > addtime(utc_timestamp(),'6:56')
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
