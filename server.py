#!/usr/bin/env python3

import sys, os
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
		self.save_pid()
		httpd.serve_forever()
		print("Serving") # will never printed
		
	def save_pid(self):
		with open("./test/server_pid.txt", "w") as server_pid_file:
			server_pid_file.write(str(os.getpid()))
			server_pid_file.close()
		
		
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
		except Exception as e:
			print("The Exception " + str(e) + " is accured.")
		finally:
			exit()
			
ss = ServerStarter()
ss.start()