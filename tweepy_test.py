#coding: utf-8
import tweepy
import webbrowser

consumer_key = 'HhFnDkO26i4Ct491Q5Zeg'
consumer_secret = 'XGNL9HqyEvO3AQtX9dMeZSsdeRY7LwjOPYnz2TcFB0'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
webbrowser.open(auth.get_authorization_url())
pin = input('PIN: ').strip()
auth.get_access_token(pin)
auth.set_access_token(auth.access_token.key, auth.access_token.secret)
api = tweepy.API(auth_handler=auth)
me = api.me()
print(me.screen_name)
