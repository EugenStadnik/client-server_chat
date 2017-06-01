#!/usr/bin/env python3

import sys
from param_parser import ParamParser
from http.server import HTTPServer, CGIHTTPRequestHandler
 
class Server:

	VERSION = "1.0.1"
	
	def __init__(self, host):
		self.host = host

	def start_server(self, host, port):
		server_address = (host, port)
		httpd = HTTPServer(server_address, CGIHTTPRequestHandler)
		print("The server is waiting for requests")
		httpd.serve_forever()
		
class ServerStarter:
	
	def start(self): 
		s = Server("127.0.0.1")
		pp = ParamParser(Server.VERSION)
		parser = pp.parse_server_param()
		namespace = parser.parse_args(sys.argv[1:])
		try:
			s.start_server(s.host, namespace.port)
		except OverflowError:
			print("The parameter is out of range. Valid parameters range - 0...65535")
			parser.print_help()
		except KeyboardInterrupt:
			print("See you next time. Bye-bye!")
		finally:
			exit()
			
ss = ServerStarter()
ss.start()