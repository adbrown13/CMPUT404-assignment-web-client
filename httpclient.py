#!/usr/bin/env python
# coding: utf-8
# Copyright 2013 Abram Hindle, Ashley Fegan
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib
from urlparse import urlparse

def help():
	print "httpclient.py [GET/POST] [URL]\n"

class HTTPRequest(object):
	def __init__(self, code=200, body=""):
		self.code = code
		self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

	def connect(self, host, port):
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		except socket.error:
			print 'Failed to create socket'
			sys.exit() 
		try:
			remote_ip = socket.gethostbyname( host )
		except socket.gaierror:
			print 'Hostname could not be resolved. Exiting'
			sys.exit()
		s.connect((remote_ip , port)) 
		return s

	def get_code(self, data):
		code =data.split()[1]
		return int(code)

	def get_headers(self,data):
		return None

	def get_body(self, data):
		body =data.split('\r\n\r\n')[1]
		return body

    # read everything from the socket
	def recvall(self, sock):
		buffer = bytearray()
		done = False
		while not done:
			part = sock.recv(1024)
			if (part):
				buffer.extend(part)
			else:
				done = not part
		return str(buffer)

	def GET(self, url, args=None):
		host= urlparse(url).hostname
		if host == None:
			host='localhost'
		port= urlparse(url).port
		if port == None:
			port=80
		s=self.connect(host,port)
		message = "GET "+urlparse(url).path+" HTTP/1.1\r\nHost: "+host+"\r\nConnection: close\r\n\r\n"
		print message
		try :
			s.sendall(message)
		except socket.error:
			print 'Send failed'
			sys.exit()
		print 'Message send successfully'
		reply = self.recvall(s)
		s.close()
		code=self.get_code(reply)
		body=self.get_body(reply)
		return HTTPRequest(code, body)

	def POST(self, url, args=None):
		host= urlparse(url).hostname
		if host == None:
			host='localhost'
		port= urlparse(url).port
		if port == None:
			port=80
		s=self.connect(host,port)
		if args==None:
			message = "POST "+urlparse(url).path+" HTTP/1.1\r\n\r\n"
		else:
			message = "POST "+urlparse(url).path+" HTTP/1.1\r\nContext-Type: application/x-www-form-urlencoded\r\nContent-Length: "+str(len( urllib.urlencode(args)))+"\r\n\r\n"+urllib.urlencode(args)+"\r\n"
		try :
			s.sendall(message)
		except socket.error:
			print 'Send failed'
			sys.exit()
		print 'Message send successfully'
		reply = self.recvall(s)
		s.close()
		code=self.get_code(reply)
		body=self.get_body(reply)
		return HTTPRequest(code, body)

	def command(self, url, command="GET", args=None):

		if (command == "POST"):
			return self.POST( url, args )
		else:
			return self.GET( url, args )
    
if __name__ == "__main__":
	client = HTTPClient()
	command = "GET"
	if (len(sys.argv) <= 1):
		help()
		sys.exit(1)
	elif (len(sys.argv) == 3):

		print client.command(sys.argv[2], sys.argv[1] )
	else:
		print client.command(  sys.argv[1],command )    
