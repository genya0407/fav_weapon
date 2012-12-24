#coding:utf-8
import time, random, urllib, cgi, hmac, hashlib

consumer_key = 'HhFnDkO26i4Ct491Q5Zeg'
consumer_secret = 'XGNL9HqyEvO3AQtX9dMeZSsdeRY7LwjOPYnz2TcFB0'

method = 'GET'
request_token_url = 'http://twitter.com/oauth/request_token'

params = {
	"oauth_consumer_key": consumer_key, # WEB で登録した oauth consumer key
	"oauth_signature_method": "HMAC-SHA1", # 暗号のアルゴリズム
	"oauth_timestamp": str(int(time.time())), # unixtime 
	"oauth_nonce": str(random.getrandbits(64)), # ランダム文字列
	"oauth_version": "1.0" # バージョン番号
	}

