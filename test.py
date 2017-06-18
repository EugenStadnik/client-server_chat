#!/usr/bin/env python3

import os
from multiprocessing import Process, Lock
from server import Server

def start_server(l, *server_args):
	l.acquire()
	try:
		os.system("server.py " + " ".join(map(str, server_args)))
	finally:
		l.release()
	
def f(l, i):
	l.acquire()
	try:
		print('hello world', i)
	finally:
		l.release()

if __name__ == '__main__':
	
	lock = Lock()
	p = Process(target=start_server, args=(lock, "--port=80", ">", "./test/out/server_out.txt"))
	p.start()
	#p.join()
	#p.terminate()
	Server.httpd.socket.close()