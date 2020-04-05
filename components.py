import datetime as dt
import dash_html_components as html
import dash_bootstrap_components as dbc

# class FeedData:
#     def __init__(self,id, name, username, profile_pic, follower, tweet, created_at):
#         self.id = id
#         self.name = name
#         self.username = username
#         self.profile_pic = profile_pic
#         self.follower = follower
#         self.tweet = tweet
#         self.created_at = created_at
name_style = {
    'margin': '0',
    'margin-left': '0.5em',
    'text-align': 'left'
}

username_style = {
    'margin': '0',
    'margin-left': '1.5em',
    'text-align': 'left'
}

image_style = {
    'border-radius': '50%',
    'margin-left': '1em'
}

image_verified_style = {
    'width': '1em',
    'heigth': 'auto',
    'margin-left': '0.25em',
    'margin-top': '0.25em'
}

verified_logo = 'https://upload.wikimedia.org/wikipedia/commons/e/e4/Twitter_Verified_Badge.svg'


def feed_content_generator(data):
    id = data.index.values[0]
    src = data.profile_pic.values[0]
    name = data.name.values[0]
    username = data.username.values[0]
    tweet = data.tweet.values[0]
    created_at = dt.datetime.strptime(data.local_time.values[0], '%Y-%m-%d %H:%M:%S').strftime('%A %d %B %Y | %H:%M')
    return dbc.CardBody([
        dbc.Row([
            html.Img(src=src, id='img-{}'.format(id), style=image_style),
            html.Div(
                [
                    html.H5(name, id='name-{}'.format(id), style=name_style),
                    dbc.Row([html.P(username, id='username-{}'.format(id), style=username_style),
                             html.Img(src=verified_logo, style=image_verified_style),
                             ])
                ]),

        ],
            className="card-title"),
        html.P(tweet, id='tweet-{}'.format(id)),
        html.P(html.Em(created_at, id='created-{}'.format(id)), style={'text-align': 'right'})
    ])
