#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time, random, urllib, cgi, hmac, hashlib, base64, sys, webbrowser, urllib.request

class twitter(object):
	def __init__(self):
		self.consumer_key = 'HhFnDkO26i4Ct491Q5Zeg'
		self.consumer_secret = 'XGNL9HqyEvO3AQtX9dMeZSsdeRY7LwjOPYnz2TcFB0'
		
		self.method = 'GET'
		self.method_2 = 'POST'

		self.request_token_url = 'http://twitter.com/oauth/request_token'
		self.access_token_url = 'http://api.twitter.com/oauth/access_token'
		
		self.token = self.get_oauth_token()
		
	def get_oauth_token(self): 
		params = {
			"oauth_consumer_key": self.consumer_key,
			"oauth_signature_method": "HMAC-SHA1", 
			"oauth_timestamp": str(int(time.time())),  
			"oauth_nonce": str(random.getrandbits(64)),
			"oauth_version": "1.0"
			}

		params_str = '&'.join(['%s=%s' % (urllib.parse.quote(key, ''),urllib.parse.quote(params[key], '')) for key in sorted(params)])
		message = '%s&%s&%s' % (self.method,urllib.parse.quote(self.request_token_url,''), urllib.parse.quote(params_str,''))
	 
		key = "%s&%s" % (self.consumer_secret, '')

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

		pin = input("PIN:").strip()
		
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

	def return_token(self):
		return self.token

def main():
	token = twitter().return_token()
	print(token[0])
	print(token[1])

if __name__ == '__main__':
	main()
