#!/usr/bin/env python3

import sys
from param_parser import ParamParser
import re
from http.client import HTTPConnection
from urllib.parse import urlencode

class Client:
	
	VERSION = "1.0.2"
	
	def __init__(self, host):
		self.host = host

	def do_post(self, message_queue):
		params = urlencode({'message':message_queue[0], 'queue':message_queue[1]})
		headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
		connection = HTTPConnection("127.0.0.1", 80)
		connection.request("POST", "/cgi-bin/receive.py", params, headers)
		response = connection.getresponse()
		data = response.read()
		data = re.search(r"\[done\]", str(data)).group(0)
		print(data)
		connection.close()

	def do_get(self, queue):
		connection = HTTPConnection('127.0.0.1', 80)
		connection.request('GET', '/cgi-bin/send.py?&queue=' + str(queue[0]))
		response = connection.getresponse()
		data = response.read()
		if re.search(r"b'([\w\W]+)\\r\\n\[done\]", str(data)):
			message = re.search(r"b'([\w\W]+)\\r\\n\[done\]", str(data)).group(1)
			print(message)
		status = re.search(r"(\[done\])", str(data)).group(1)
		print(status)
		connection.close()

class ClientStarter:
				
	def start(self):
		c = Client("127.0.0.1")
		pp = ParamParser(Client.VERSION)
		parser = pp.parse_client_param()
		namespace = parser.parse_args(sys.argv[1:])
		if namespace.command == "post":
			self.catchCRE(parser, c.do_post, namespace.message, namespace.queue)
		elif namespace.command == "get":
			self.catchCRE(parser, c.do_get, namespace.queue)
		else:
			parser.print_help()
	
	def catchCRE(self, parser, func, *args):
		try:
			func(args)
		except ConnectionRefusedError:
			print("The server is unreachable. First of all start \'server.py\'")
			parser.print_help()
			exit()
	
cs = ClientStarter()
cs.start()