import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import datetime as dt
from queries import *
from components import feed_content_generator
from multiprocessing import Process
from tweet_streamer import start_stream

external_stylesheets = [dbc.themes.SUPERHERO]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

cardheader_style = {
    'font-size': '1em',
    'padding': '0.5em 0em 0.5em 1em',
}
card_style = {
    'padding': '0.5em 0.5em',
}
axis_length = 1
iter = range(4)
dash_link = 'https://plotly.com/dash/'
twitter_link = 'https://developer.twitter.com/en/docs/api-reference-index'
ln_link = 'https://www.linkedin.com/in/kevin-sukaria-23a155137/'

df = dataframe_creation(query)
latest_tweet = dataframe_creation(latest_tweet_query)
user_count = dataframe_creation(user_count_query)
df_hour = dataframe_creation(today_hourly_query)

df.created_at = pd.to_datetime(df.created_at) + dt.timedelta(hours=7)
latest_tweet.created_at = pd.to_datetime(latest_tweet.created_at) + dt.timedelta(hours=7)

x_max = df.created_at.max()
x_min = df.created_at.max() - dt.timedelta(minutes=axis_length)
total_tweets = f'{user_count.total_count.sum():,}'
average_tweets = round(df.tweet_count.mean(), 2)
user = f'{user_count.distinct_user.max():,}'
tweet_per_user = round(user_count.total_count.sum() / user_count.distinct_user.max(), 2)

fig = px.line(
    df,
    x="created_at",
    y="tweet_count",
    # color="Status",
    range_x=[x_min, x_max],
    # range_y=[0, df.tweet_count.max() * 1.2],
)
fig.update_layout(
    {

        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'font': {'color': 'white'},
        'xaxis': {'showgrid': False, 'title_text': 'Time when the tweets are created'},
        'yaxis': {'showgrid': False, 'title_text': 'Tweet count'}
    }
)

bar_fig = px.line(
    df_hour,
    x="hour",
    y="tweet_count",
    # color='Status',
    range_x=[-1, 25],
    # range_y=[0, 1.2 * df_hour.tweet_count.max()],
)
bar_fig.update_layout(
    {
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'font': {'color': 'white'},
        'xaxis': {'dtick': 1, 'showgrid': False, 'title_text': 'Hour when the tweets are created'},
        'yaxis': {'showgrid': False, 'title_text': 'Tweet count'}
    }
)

card_content0 = [
    dbc.CardHeader("Total Tweets ", style=cardheader_style),
    dbc.CardBody(html.H4(total_tweets, id='card-0', className="card-title"))
]

card_content1 = [
    dbc.CardHeader("Tweets / Sec ", style=cardheader_style),
    dbc.CardBody(html.H4(average_tweets, id='card-1', className="card-title"))
]

card_content2 = [
    dbc.CardHeader("Unique Users ", style=cardheader_style),
    dbc.CardBody(html.H4(user, id='card-2', className="card-title"))
]

card_content3 = [
    dbc.CardHeader("Tweets / User", style=cardheader_style),
    dbc.CardBody(html.H4(tweet_per_user, id='card-3', className="card-title"))
]

latest_card0 = feed_content_generator(latest_tweet.iloc[[0]])
latest_card1 = feed_content_generator(latest_tweet.iloc[[1]])
latest_card2 = feed_content_generator(latest_tweet.iloc[[2]])
latest_card3 = feed_content_generator(latest_tweet.iloc[[3]])
latest_card4 = feed_content_generator(latest_tweet.iloc[[4]])

app.layout = dbc.Container(
    fluid=True,
    children=[
        html.Div([
            html.H1('COVID-19 Tweet Streamer', style={'text-align': 'center'}),
            html.P([
                "This is a simple ",
                html.A(html.Strong('Dash'), href=dash_link),
                " web application that streams today's tweets about COVID-19 through ",
                html.A(html.Strong('official Twitter API'), href=twitter_link),
                ", Timezone used : GMT+7"],
            ),
            html.P(
                ['Creator : ',
                 html.A(html.Strong('Kevin Sukaria'), href=ln_link)],
            )],
            style={'background-color': 'black', 'margin': '0 0 1em 0', 'text-align': 'center', 'padding': '0.5em 0'}),
        dcc.Interval(
            id='interval-component',
            interval=2 * 1000,  # in milliseconds
            n_intervals=0
        ),
        dcc.Interval(
            id='interval-component2',
            interval=15 * 1000,  # in milliseconds
            n_intervals=0
        ),

        dcc.Interval(
            id='interval-component3',
            interval=43200 * 1000,  # in milliseconds
            n_intervals=0
        ),
        html.Div(id='hidden-div', style={'display': 'none'}),

        dbc.Row([
            dbc.Col([
                dbc.Row([
                    dbc.Col(dbc.Card(card_content0), md=3, xs=6, style=card_style),
                    dbc.Col(dbc.Card(card_content1), md=3, xs=6, style=card_style),
                    dbc.Col(dbc.Card(card_content2), md=3, xs=6, style=card_style),
                    dbc.Col(dbc.Card(card_content3), md=3, xs=6, style=card_style)
                ],
                    no_gutters=True),

                dbc.Col(dbc.Card([dbc.CardHeader("Live Tweet Count per Second"),
                                  dcc.Graph(
                                      id='line',
                                      figure=fig,
                                      animate=False

                                  )
                                  ]), style=card_style),

                dbc.Col(dbc.Card([dbc.CardHeader("Hourly Tweet Count"),
                                  dcc.Graph(
                                      id='bar',
                                      figure=bar_fig,
                                      animate=True
                                  )
                                  ]), style=card_style)
            ], lg=7, xs=12, style={'margin-right': '-1em'}),
            dbc.Col([
                html.H4('Latest Tweets from Verified Users'),
                html.P('Feeds are refreshed around every 15 seconds'),
                dbc.Card(latest_card0, style={'margin-bottom': '0.25em'}),
                dbc.Card(latest_card1, style={'margin-bottom': '0.25em'}),
                dbc.Card(latest_card2, style={'margin-bottom': '0.25em'}),
                dbc.Card(latest_card3, style={'margin-bottom': '0.25em'}),
                dbc.Card(latest_card4, style={'margin-bottom': '0.25em'})
            ],
                lg=5, xs=12, style={'margin': '0.5em 0em'}
            )
        ]),

    ])

card_output = [Output('card-{}'.format(val), 'children') for val in iter]
line_output = [Output('line', 'figure')]
output1 = card_output + line_output


@app.callback(output1, [Input('interval-component', 'n_intervals')])
def update_graph(n):
    df = dataframe_creation(query)
    user_count = dataframe_creation(user_count_query)

    df.created_at = pd.to_datetime(df.created_at) + dt.timedelta(hours=7)
    x_max = df.created_at.max()
    x_min = df.created_at.max() - dt.timedelta(minutes=axis_length)

    total_tweets = f'{user_count.total_count.sum():,}'
    average_tweets = round(df.tweet_count.mean(), 2)
    user = f'{user_count.distinct_user.max():,}'
    tweet_per_user = round(user_count.total_count.sum() / user_count.distinct_user.max(), 2)

    fig = px.line(
        df,
        x="created_at",
        y="tweet_count",
        # color='Status',
        range_x=[x_min, x_max],
        # range_y=[0, df.tweet_count.max() * 1.2],
    )
    fig.update_layout(
        {
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'font': {'color': 'white'},
            'xaxis': {'showgrid': False, 'title_text': 'Time when the tweets are created'},
            'yaxis': {'showgrid': False, 'title_text': 'Tweet count'}
        }
    )

    return total_tweets, average_tweets, user, tweet_per_user, fig


input2 = [Input('interval-component2', 'n_intervals')]
name_output = [Output('name-{}'.format(val), 'children') for val in iter]
user_output = [Output('username-{}'.format(val), 'children') for val in iter]
img_output = [Output('img-{}'.format(val), 'src') for val in iter]
created_output = [Output('created-{}'.format(val), 'children') for val in iter]
tweet_output = [Output('tweet-{}'.format(val), 'children') for val in iter]
bar_output = [Output('bar', 'figure')]
output2 = name_output + user_output + img_output + created_output + tweet_output + bar_output


@app.callback(output2, input2)
def update_feed(n):
    df_hour = dataframe_creation(today_hourly_query)
    latest_tweet = dataframe_creation(latest_tweet_query)
    latest_tweet.created_at = pd.to_datetime(latest_tweet.created_at) + dt.timedelta(hours=7)
    bar_fig = px.bar(
        df_hour,
        x="hour",
        y="tweet_count",
        # color='Status',
        range_x=[-1, 25],
        # range_y=[0, 1.2 * df_hour.tweet_count.max()],
    )
    bar_fig.update_layout(
        {
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'font': {'color': 'white'},
            'xaxis': {'dtick': 1, 'showgrid': False, 'title_text': 'Hour when the tweets are created'},
            'yaxis': {'showgrid': False, 'title_text': 'Tweet count'}
        }
    )

    name = [latest_tweet.name[val] for val in iter]
    username = [latest_tweet.username[val] for val in iter]
    img = [latest_tweet.profile_pic[val] for val in iter]
    created = [pd.to_datetime(latest_tweet.local_time.values[val]).strftime('%A %d %B %Y | %H:%M')
               for val in iter]
    tweet = [latest_tweet.tweet[val] for val in iter]
    fig = [bar_fig]
    output = name + username + img + created + tweet + fig

    return output


@app.callback(Output('hidden-div', 'style'), [Input('interval-component3', 'n_intervals')])
def clear_db(n):
    db_clear(delete_query)
    return {'display': 'none'}


if __name__ == '__main__':
    # p1 = Process(target=start_app)
    # p1.start()
    app.run_server(host="127.0.0.1", port=8080, debug=True)
    # p2 = Process(target=start_stream)
    # p2.start()
