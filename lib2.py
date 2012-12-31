#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time, random, urllib, cgi, hmac, hashlib, base64, sys, webbrowser, json,requests

class twitter(object):
	def __init__(self,token=None):
		self.consumer_key = 'HhFnDkO26i4Ct491Q5Zeg'
		self.consumer_secret = 'XGNL9HqyEvO3AQtX9dMeZSsdeRY7LwjOPYnz2TcFB0'

		self.method = 'GET'
		self.method_2 = 'POST'

		self.request_token_url = 'http://twitter.com/oauth/request_token'
		self.access_token_url = 'http://api.twitter.com/oauth/access_token'
		self.update_url = 'https://api.twitter.com/1.1/statuses/update.json'
		self.home_timeline_url = 'https://api.twitter.com/1.1/statuses/home_timeline.json'
		self.user_timeline_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
		self.create_fav_url = 'https://api.twitter.com/1.1/favorites/create.json'

		if token == None :
			token = self.get_oauth_token()
			
		self.access_token = token[0]
		self.access_token_secret = token[1]
		
		self.params = {
			'oauth_consumer_key': self.consumer_key,
			'oauth_signature_method': 'HMAC-SHA1',
			'oauth_timestamp': str(int(time.time())), 
			'oauth_nonce': str(random.getrandbits(64)),
			'oauth_version': '1.0'       }
	
	def params_str(self,params):
		return '&'.join(['%s=%s' % (urllib.parse.quote(key, ''),urllib.parse.quote(params[key], '~')) for key in sorted(params)])
	
	def gen_message(self,method,url,params):
		return '%s&%s&%s' % (method,urllib.parse.quote(url,''), urllib.parse.quote(self.params_str(params),''))
	
	def gen_sig_digest64(self,key,message):
		hm = hmac.new(key.encode(),message.encode(),hashlib.sha1)
		return base64.b64encode(hm.digest())
	
	def gen_header_str(self,params):
		return 'OAuth ' + ','.join(['%s=%s' % (urllib.parse.quote(key,''),urllib.parse.quote(params[key],'~')) for key in sorted(params)])
	
	def get_oauth_token(self): 
		params = {
			'oauth_consumer_key': self.consumer_key,
			'oauth_nonce': str(random.getrandbits(64)),
			'oauth_signature_method': 'HMAC-SHA1', 
			'oauth_timestamp': str(int(time.time())),  
			'oauth_version': '1.0'
			}
		
		params_str = '&'.join(['%s=%s' % (urllib.parse.quote(key, ''),urllib.parse.quote(params[key], '')) for key in sorted(params)])
		message = '%s&%s&%s' % (self.method,urllib.parse.quote(self.request_token_url,''), urllib.parse.quote(params_str,''))
		print(message)
		key = '%s&%s' % (self.consumer_secret, '')

		signature = hmac.new(key.encode(), message.encode(), hashlib.sha1)

		digest_base64 = base64.b64encode(signature.digest().strip())

		params['oauth_signature'] = digest_base64

		_url = self.request_token_url+ '?' + urllib.parse.urlencode(params)

		result = urllib.request.urlopen(_url).read()

		data = cgi.parse_qs(result)
		
		return self.get_access_token(data)

	def get_access_token(self, data): 
		
		oauth_token_url ='http://api.twitter.com/oauth/authorize' + '?oauth_token=' + data[b'oauth_token'][0].decode()
		webbrowser.open(oauth_token_url)

		pin = input('PIN:').strip()
		
		params = {
			'oauth_consumer_key':self.consumer_key,
			'oauth_nonce':str(random.getrandbits(64)),
			'oauth_signature_method':'HMAC-SHA1',
			'oauth_timestamp':str(int(time.time())),
			'oauth_token':data[b'oauth_token'][0].decode(),
			'oauth_verifier':pin,
			'oauth_version':'1.0'
			}
		
		params_str = '&'.join(['%s=%s' % (urllib.parse.quote(key, ''),urllib.parse.quote(params[key], '')) for key in sorted(params)])
		message = '%s&%s&%s' % (self.method_2, urllib.parse.quote(self.access_token_url,''), urllib.parse.quote(params_str,'') )

		key = urllib.parse.quote(self.consumer_secret,'') + '&' + urllib.parse.quote(data[b'oauth_token_secret'][0].decode(),'')

		signature = hmac.new(key.encode(), message.encode(), hashlib.sha1)

		params['oauth_signature'] = base64.b64encode(signature.digest().strip())

		_url = self.access_token_url + '?' + urllib.parse.urlencode(params)

		result = urllib.request.urlopen(_url).read()
		token = cgi.parse_qs(result)
		
		return [token[b'oauth_token'][0].decode(), token[b'oauth_token_secret'][0].decode()] #[access_token, access_token_secret]

	def update_status(self, text):
		params = self.params
		params['oauth_token'] = self.access_token
		params['status'] = text
		
		message = self.gen_message(self.method_2,self.update_url,params)
		
		key = '%s&%s' % (self.consumer_secret, self.access_token_secret)

		params['oauth_signature'] = self.gen_sig_digest64(key,message)
		
		del params['status']
		
		header_params_str = self.gen_header_str(params)
		
		data = 'status='+urllib.parse.quote(text)
		
		req = urllib.request.Request(self.update_url)
		req.add_header('Authorization',header_params_str)
		req.add_data(data.encode())
		res = urllib.request.urlopen(req)

	def home_timeline(self):
		params = self.params
		params['oauth_token'] = self.access_token
		
		message = self.gen_message(self.method,self.home_timeline_url,params)
		key = '%s&%s' % (self.consumer_secret, self.access_token_secret)
		
		params['oauth_signature'] = self.gen_sig_digest64(key,message)
		
		req = urllib.request.Request(self.home_timeline_url)
		req.add_header('Authorization',self.gen_header_str(params))

		res = urllib.request.urlopen(req)

	def user_timeline(self,target):
		params = self.params
		params['oauth_token'] = self.access_token
		params['screen_name'] = target
		
		message = self.gen_message(self.method,self.user_timeline_url,params)
		key = '%s&%s' % (self.consumer_secret,self.access_token_secret)
		
		params['oauth_signature'] = self.gen_sig_digest64(key,message)
		del params['screen_name']
		
		req_url = self.user_timeline_url + '?screen_name=' + urllib.parse.quote(target)
		
		req = urllib.request.Request(req_url)
		req.add_header('Authorization',self.gen_header_str(params))
		
		print(self.gen_header_str(params))
		
		return json.loads(urllib.request.urlopen(req).read().decode())
		
	def create_fav(self,tweet_id):
		params = {
			'oauth_consumer_key': self.consumer_key,
			'oauth_signature_method': 'HMAC-SHA1',
			'oauth_timestamp': str(int(time.time())), 
			'oauth_nonce': str(random.getrandbits(64)),
			'oauth_version': '1.0' 
			}
		params['oauth_token'] = self.access_token
		params['id'] = tweet_id
		
		message = self.gen_message(self.method_2,self.create_fav_url,params)
		key = '%s&%s' % (self.consumer_secret,self.access_token_secret)
				
		params['oauth_signature'] = self.gen_sig_digest64(key,message)
		
		print(message)
		
		del params['id']
		
		print(self.gen_header_str(params))
		
		data = 'id=' + urllib.parse.quote(tweet_id)
		
		req = urllib.request.Request(self.create_fav_url)
		req.add_header('Authorization',self.gen_header_str(params))
		req.add_data(data.encode())	
		
		try :
			urllib.request.urlopen(req)
		except urllib.error.HTTPError as e :
			if e.code == '403' :
				print('You have already faved it')
			else :
				print(e.code)
				print(e.read())
		
def main():
	
	tw = twitter(['264147645-UUHUOZNxK0aPqSvXoW4mwG1zLrqmcTbCs1gMDnEA','cvcUfJtcWwYttQjhRYvzKOwWOurAuEuFWnQyLS39E'])
	tw.user_timeline('countboo')
	
	#t = twitter()
	#ついーと
	#tw.update_status('関数の命名センスのかけらもない')
	'''
	
	twlist = tw.user_timeline('countboo')
	idlist = []
	for i in twlist :
		idlist.append(i['id_str'])
	
	for i in idlist :
		tw.create_fav(i)
	'''
	#print(twlist[0]['id_str'])

if __name__ == '__main__':
	main()
