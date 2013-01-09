# coding:utf-8
try:
	import time, random, urllib.request, urllib.parse, cgi, hmac, hashlib, base64, webbrowser, json, pickle
except:
	print('Error : Lack of libraries')

CONSUMER_KEY = 'HhFnDkO26i4Ct491Q5Zeg'
CONSUMER_SECRET = 'XGNL9HqyEvO3AQtX9dMeZSsdeRY7LwjOPYnz2TcFB0'
REQUEST_TOKEN_URL = 'http://twitter.com/oauth/request_token'
OAUTH_AUTHORIZE_URL = 'http://api.twitter.com/oauth/authorize'
ACCESS_TOKEN_URL = 'http://api.twitter.com/oauth/access_token'
USER_TIMELINE_URL = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
FAV_URL = 'https://api.twitter.com/1.1/favorites/create.json'

PARAMS = {
	'oauth_consumer_key': CONSUMER_KEY,
	'oauth_signature_method': 'HMAC-SHA1',
	'oauth_timestamp': str(int(time.time())), 
	'oauth_nonce': str(random.getrandbits(64)),
	'oauth_version': '1.0'
}

class twitter(object):
	def gen_message(self,method,url,params): # methodとurlとparamsを渡すとmessageを返す
		method = urllib.parse.quote(method)
		url = urllib.parse.quote(url,'')
		params_str ='&'.join(['%s=%s' % (urllib.parse.quote(key, ''),
										urllib.parse.quote(params[key], '~')) 
										for key in sorted(params)])
		params_str = urllib.parse.quote(params_str,'')
		return method + '&' + url + '&' + params_str
	
	def gen_signature(self,key,message): # keyとmessageを渡すとsignatureを返す
		hm = hmac.new(key.encode(),message.encode(),hashlib.sha1)
		return base64.b64encode(hm.digest().strip())
	
	def get_request_token(self): # 引数なし　request_token と request_token_secretを返す
		# パラメーターを生成
		params = PARAMS.copy()
		
		# パラメーターを元にsignatureを生成
		key = CONSUMER_SECRET + '&'
		message = self.gen_message('GET',REQUEST_TOKEN_URL,params)

		signature = self.gen_signature(key,message)
		
		# パラメーターにsignatureを追加
		params['oauth_signature'] = signature
		
		# URLを生成。　GETメソッドなので、パラメーターはURLの後ろに?で繋げる
		params = urllib.parse.urlencode(params)
		url = REQUEST_TOKEN_URL + '?' + params
		
		# oauth_token と oauth_token_secret を取得
		result = urllib.request.urlopen(url).read()
		oauth_token = cgi.parse_qs(result)[b'oauth_token'][0].decode()
		oauth_token_secret = cgi.parse_qs(result)[b'oauth_token'][0].decode()
		
		# return
		return (oauth_token , oauth_token_secret)
	
	def get_verifier(self,oauth_token): # oauth_token を入れると、ブラウザが起動してverifierを表示する
		return OAUTH_AUTHORIZE_URL + '?oauth_token=' + oauth_token

	def gen_header_str(self,params):
		return 'OAuth ' + ','.join(['%s=%s' % (urllib.parse.quote(key,''),urllib.parse.quote(params[key],'~')) for key in sorted(params)])
	
	def get_user_dict(self,oauth_token,oauth_token_secret,verifier): # oauth_token,oauth_token_secret,verifierを入れるとaccess_token,access_token_secret,screen_nameを返す
		# パラメータの準備
		params = PARAMS.copy()
		params['oauth_token'] = oauth_token
		params['oauth_verifier'] = verifier
		
		# パラメーターからsignarureを生成
		key = CONSUMER_SECRET + '&' + oauth_token_secret
		message = self.gen_message('GET',ACCESS_TOKEN_URL,params)
		signature = self.gen_signature(key,message)
		
		# パラメーターにsignatureを追加
		params['oauth_signature'] = signature
		
		# URLを生成。 GETメソッドなので、パラメータはURLの後ろに以下略
		params = urllib.parse.urlencode(params)
		url = ACCESS_TOKEN_URL + '?' + params
		
		# access_token と access_token_secret と screen_nameを取得
		result = urllib.request.urlopen(url).read()
		access_token = cgi.parse_qs(result)[b'oauth_token'][0].decode()
		access_token_secret = cgi.parse_qs(result)[b'oauth_token_secret'][0].decode()
		screen_name = cgi.parse_qs(result)[b'screen_name'][0].decode()
		
		# user_dict 生成
		user_dict = {
			'access_token':access_token,
			'access_token_secret':access_token_secret,
			'screen_name':screen_name
			# 'icon':そのうち入れるかもしれないけどめんどくさいから後回し
		}
		return user_dict

	def get_user_timeline(self,user_dict,target,count):
		# 署名
		option = {
			'screen_name':target,
			'include_rts':'false',
			'count':count
		}
		params = PARAMS.copy()
		params['oauth_token'] = user_dict['access_token']
		params.update(option)
		
		key = '%s&%s' % (CONSUMER_SECRET,user_dict['access_token_secret'])
		message = self.gen_message('GET',USER_TIMELINE_URL,params)
		
		signature = self.gen_signature(key,message)
		
		# ヘッダ
		params = PARAMS.copy()
		params['oauth_token'] = user_dict['access_token']
		params['oauth_signature'] = signature
		header_oauth = self.gen_header_str(params)
		
		# リクエスト生成
		url = USER_TIMELINE_URL + '?' + urllib.parse.urlencode(option)
		req = urllib.request.Request(url)
		req.add_header('Authorization',header_oauth)
		
		result = urllib.request.urlopen(req).read().decode()
		
		tweets = json.loads(result)
		
		ids = []
		for t in tweets:
			ids.append(t['id_str'])
		return ids
	
	def create_fav(self,user_dict,tweet_id):
		# 署名
		option = {
			'id':tweet_id
		}
		params = PARAMS.copy()
		params['oauth_token'] = user_dict['access_token']
		params.update(option)
		message = self.gen_message('POST',FAV_URL,params)
		key = '%s&%s' % (CONSUMER_SECRET,user_dict['access_token_secret'])
		signature = self.gen_signature(key,message)
		
		#ヘッダ
		params =PARAMS.copy()
		params['oauth_token'] = user_dict['access_token']
		params['oauth_signature'] = signature
		header = self.gen_header_str(params)
		
		#データ
		data = urllib.parse.urlencode(option)
		
		#リクエスト生成
		url = FAV_URL
		req = urllib.request.Request(url)
		req.add_header('Authorization',header)
		req.add_data(data.encode())
		
		# urlopen
		try :
			urllib.request.urlopen(req)
		except :
			pass # すでにfavったツイートとかを踏んでしまった時の対応は後で考えよう。
