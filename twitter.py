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
	def __init__(self):
		try:
			with open('./users','rb') as f:
				self.users_list = f.pickle.load(f)
		except:
			print('ユーザーが設定されていません。認証を行なってください')
		
	def get_signature(self,method,url,key,data=None):
		params = PARAMS.copy()
		if data:
			for key in sorted(data):
				params[key] = data[key]
		
		url = urllib.parse.quote(url,'')
		params_str = '&'.join(['%s=%s' % (urllib.parse.quote(key, ''),
										urllib.parse.quote(params[key], '~')) 
										for key in sorted(params)])
		params_str = urllib.parse.quote(params_str,'')
		message = method + '&' + url + '&' + params_str
		print(message)
		hm = hmac.new(key.encode(),message.encode(),hashlib.sha1)
		
		return base64.b64encode(hm.digest().strip())

	def gen_header(self,url,params):
		auth = 'OAuth ' + ','.join(['%s=%s' % (urllib.parse.quote(key,''),urllib.parse.quote(params[key],'~')) for key in sorted(params)])
		print(auth)
		req = urllib.request.Request(url)
		req.add_header('Authorization',auth)
		return req

	def get_access_token(self):
		#RequestTokenを取得
		params = PARAMS.copy()
		params['oauth_signature'] = self.get_signature('GET',REQUEST_TOKEN_URL,CONSUMER_SECRET + '&')
		
		argument = urllib.parse.urlencode(params)
		url = REQUEST_TOKEN_URL + '?' + argument
		
		res = urllib.request.urlopen(url).read()
		oauth_token = cgi.parse_qs(res)[b'oauth_token'][0].decode()
		oauth_token_secret = cgi.parse_qs(res)[b'oauth_token_secret'][0].decode()
		
		#AccessTokenを取得
		url = OAUTH_AUTHORIZE_URL + '?oauth_token=' + oauth_token
		webbrowser.open(url)
		
			#デバッグコード#
		pin = input('PIN:').strip()
				
		extended_params = {
			'oauth_token':oauth_token,
			'oauth_verifier':pin
			}
		
		params = PARAMS.copy()
		key = CONSUMER_SECRET + '&' + oauth_token_secret
		key = urllib.parse.quote(key)
		params['signature'] = self.get_signature('POST',ACCESS_TOKEN_URL,key,data=extended_params)
		params.update(extended_params)
		argment = urllib.parse.urlencode(params)
		url = ACCESS_TOKEN_URL + '?' + argment
		res = cgi.parse_qs(urllib.request.urlopen(url).read())
		
		return (res[b'screen_name'][0].decode(),res[b'oauth_token'][0].decode(),res[b'oauth_token_secret'][0].decode()) #(token,secret)

	def user_timeline(self,token,token_secret,target,count='20'):
		params = PARAMS.copy()
		key = '%s&%s' % (CONSUMER_SECRET,token_secret)
		extended_params = {
			'oauth_token':token,
			'screen_name':target,
			'count':count
		}
		params['oauth_signature'] = self.get_signature('GET',USER_STREAM_URL,key,data=extended_params)
		params['oauth_token'] = token
		arg_params = {
			'screen_name':target,
			'count':count
			}
		argment = urllib.parse.urlencode(arg_params)
		print(argment)
		url = USER_STREAM_URL + '?' + argment
		print(url)
		req = self.gen_header(url,params)
		res = urllib.request.urlopen(req).read()
		tweets = json.loads(res.decode())
		
		return tweets

def main():
	tw = twitter()
	screen_name,access_token,access_token_secret = tw.get_access_token()
	print(access_token)
	a = tw.user_timeline(access_token,access_token_secret,'countboo')
	
if __name__ == '__main__':
	main()
