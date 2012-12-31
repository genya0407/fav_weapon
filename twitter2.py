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
USER_STREAM_URL = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
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
		url = urllib.parse.quote(url)
		params_str ='&'.join(['%s=%s' % (urllib.parse.quote(key, ''),
										urllib.parse.quote(params[key], '~')) 
										for key in sorted(params)])
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
		params['signature'] = signature
		
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
		webbrowser(OAUTH_AUTHORIZE_URL + '?oauth_token=' + oauth_token)
	
	def get_access_token(self,oauth_token,oauth_token_secret,verifier): # oauth_token,oauth_token_secret,verifierを入れるとaccess_token,access_token_secret,screen_nameを返す
		# パラメータの準備
		params = PARAMS.copy()
		params['oauth_token'] = oauth_token
		params['oauth_verifier'] = verifier
		
		# パラメーターからsignarureを生成
		key = CONSUMER_SECRET + '&' + oauth_token_secret
		message = self.gen_message('GET',ACCESS_TOKEN_URL,params)
		signarure = self.gen_signature(key,message)
		
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
		
		# return
		return (access_token,access_token_secret,screen_name)
	
