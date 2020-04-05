import tweepy
import dataset
from urllib3.exceptions import ProtocolError



auth = tweepy.OAuthHandler('sTdMg4nUSf4brak6uuBOZJg4M', 'b8WQYukt00Kgl6kdTxMnx4OVlCTcD28EtsT4d2X9SOb9JomuRK')
auth.set_access_token('1392363164-8tTU3tZByrZKVg2Sq7DP7kDSaN9CKkYkJGXhpzw',
                      'woxdgDzBQ568OqGHXoItQCrs29d3LvtkZ7drL89WdX23e')

api = tweepy.API(auth)


class NewStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        name = status.user.name
        username = status.user.screen_name
        followers = status.user.followers_count
        user_location = status.user.location
        verified_status = status.user.verified
        profile_pic = status.user.profile_image_url_https
        if hasattr(status, "retweeted_status"):  # Check if Retweet
            try:
                tweet = status.retweeted_status.extended_tweet["full_text"]
            except AttributeError:
                tweet = status.retweeted_status.text
        else:
            try:
                tweet = status.extended_tweet["full_text"]
            except AttributeError:
                tweet = status.text
        language = status.lang
        hashtags = str(status.entities['hashtags'])
        retweet_count = status.retweet_count
        favorite_count = status.favorite_count
        created_at = status.created_at

        db = dataset.connect('sqlite:///tweets.db')
        table = db["tweets_stream"]
        table.insert(dict(
            name=name,
            username='@'+username,
            user_location=user_location,
            verified_status=verified_status,
            followers=followers,
            profile_pic=profile_pic,
            tweet=tweet,
            language=language,
            hashtags=hashtags,
            retweet_count=retweet_count,
            favorite_count=favorite_count,
            created_at=created_at))
        db.close()

    def on_error(self, status_code):
        if status_code == 420:
            return
        print(status_code)

    def on_exception(self, exception):
        return


print('streaming start !')
stream_listener = NewStreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
while True:
    try:
        stream.filter(track=['corona', 'virus', 'COVID-19'])
    except (ProtocolError, AttributeError):
        continue
