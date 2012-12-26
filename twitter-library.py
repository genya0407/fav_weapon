#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time, random, urllib, cgi, hmac, hashlib, base64, sys, webbrowser, urllib.request.build_opener()

consumer_key = 'HhFnDkO26i4Ct491Q5Zeg'
consumer_secret = 'XGNL9HqyEvO3AQtX9dMeZSsdeRY7LwjOPYnz2TcFB0'

# Request Token は GET で取得
method = 'GET'
method2 = 'POST'

# Request Token 取得の URL
request_token_url = 'http://twitter.com/oauth/request_token'
access_token_url = 'http://api.twitter.com/oauth/access_token'

# 必須パラメータを準備
params = {
    "oauth_consumer_key": consumer_key, # WEB で登録した oauth consumer key
    "oauth_signature_method": "HMAC-SHA1", # 暗号のアルゴリズム
    "oauth_timestamp": str(int(time.time())), # unixtime 
    "oauth_nonce": str(random.getrandbits(64)), # ランダム文字列
    "oauth_version": "1.0" # バージョン番号
    }

params2 = {
    'oauth_consumer_key':consumer_key,
    'oauth_nonce':str(random.getrandbits(64)),
    'oauth_signature_method':'HMAC-SHA1',
    'oauth_timestamp':str(int(time.time())),
    'oauth_token':data[b'oauth_token'][0].decode(),
    'oauth_verifier':pin,
    'oauth_version':'1.0'
    }

def open(url, proxy=None):
    opener = urllib.request.build_opener()
    if proxy:
        proxy_dict = {'http':proxy}
        proxy_handler = urllib.request.ProxyHandler(proxy_dict)
        opener.add_handler(proxy_handler)
    try:
        reader = opener.open(url)
        data = reader.read()
    except Exception as e:
        print('%s' % (str(e)))
        data = None
    return data

def get_oauth_token(params): #return data
    params_str = '&'.join(['%s=%s' % (urllib.parse.quote(key, ''),urllib.parse.quote(params[key], '')) for key in sorted(params)])
    message = '%s&%s&%s' % (method,urllib.parse.quote(request_token_url,''), urllib.parse.quote(params_str,''))
 
    key = "%s&%s" % (consumer_secret, '')

    signature = hmac.new(key.encode(), message.encode(), hashlib.sha1)

    digest_base64 = base64.b64encode(signature.digest().strip())

    params['oauth_signature'] = digest_base64

    _url = request_token_url+ '?' + urllib.parse.urlencode(params)

    result = open(_url)

    data = cgi.parse_qs(result)
    
    return data

oauth_token_url ='http://api.twitter.com/oauth/authorize' + '?oauth_token=' + data[b'oauth_token'][0].decode()
webbrowser.open(oauth_token_url)

pin = input('PIN:').strip()

params2 = {
    'oauth_consumer_key':consumer_key,
    'oauth_nonce':str(random.getrandbits(64)),
    'oauth_signature_method':'HMAC-SHA1',
    'oauth_timestamp':str(int(time.time())),
    'oauth_token':data[b'oauth_token'][0].decode(),
    'oauth_verifier':pin,
    'oauth_version':'1.0'
    }

params_str_2 = '&'.join(['%s=%s' % (urllib.parse.quote(key, ''),urllib.parse.quote(params2[key], '')) for key in sorted(params2)])
message_2 = '%s&%s&%s' % (method2, urllib.parse.quote(access_token_url,''), urllib.parse.quote(params_str_2,'') )

key_2 = urllib.parse.quote(consumer_secret,'') + '&' + urllib.parse.quote(data[b'oauth_token_secret'][0].decode(),'')

signature_2 = hmac.new(key_2.encode(), message_2.encode(), hashlib.sha1)

params2['oauth_signature'] = base64.b64encode(signature_2.digest().strip())

__url = access_token_url + '?' + urllib.parse.urlencode(params2)

result2 = open(__url)
data_2 = cgi.parse_qs(result2)

print(data_2)
