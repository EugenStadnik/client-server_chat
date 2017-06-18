#!/usr/bin/env python3

import os, sys, multiprocessing, time, signal, pickle

class ServerInterface:

	def start_server(self, lock, time, *server_args):
		os.chdir("..")
		os.system("python -u server.py " + " ".join(map(str, server_args)) + " > ./test/out/server_out_" + str(time) + ".txt 2>&1")
		lock.release()
	
	def start_server_process(self, lock, time, server_args):
		p = multiprocessing.Process(target=self.start_server, args=(lock, time, server_args))
		p.start()
		return p
	
	def stop_server(self, server_process):
		server_process.terminate()
		with open("server_pid.txt", "r") as server_pid_file:
			server_pid = server_pid_file.read()
			if sys.platform.startswith('linux') or sys.platform.startswith('freebsd') or sys.platform.startswith('darwin'):
				os.system("kill " + str(server_pid))
			elif sys.platform.startswith('win32') or sys.platform.startswith('cygwin'):
				os.system("tskill " + str(server_pid))
			server_pid_file.close()
			
		
		
class ClientInterface:
	
	def start_client(self, lock, time, *client_args):
		os.chdir("..")
		os.system("python -u client.py " + " ".join(map(str, client_args)) + " > ./test/out/client_out_" + str(time) + ".txt 2>&1")
		lock.release()

	def start_client_process(self, lock, time, client_args):
		client_process = multiprocessing.Process(target=self.start_client, args=(lock, time, client_args))
		client_process.start()
		client_process.join()
		client_process.terminate()

class Tester:

	def __init__(self):
		self.si = ServerInterface()
		self.ci = ClientInterface()
		self.lock = multiprocessing.Lock()
	
	def get_current_time(self):
		return time.strftime("%Y-%m-%d_%H.%M.%S", time.localtime())
	
	def test_negative_server_start(self):
		# start server without parameters
		current_time = self.get_current_time()
		self.lock.acquire()
		server_process = self.si.start_server_process(self.lock, current_time, "")
		time.sleep(5)
		with open("./out/server_out_" + str(current_time) + ".txt", 'r') as server_out_file:
			server_out = server_out_file.readlines()
			assert server_out == ['usage: server.py [-h] --port N [--version]\n', 'server.py: error: the following arguments are required: --port\n']
			server_out_file.close()
		#self.si.stop_server(server_process)
			
	def test_negative_client_start(self):
		# start client without server
		current_time = self.get_current_time()
		self.lock.acquire()
		client_process = self.ci.start_client_process(self.lock, current_time, "get")
		time.sleep(5)
		with open("./out/client_out_" + str(current_time) + ".txt", 'r') as client_out_file:
			client_out = client_out_file.readline()
			assert client_out == "The server is unreachable. First of all start 'server.py'\n"
			client_out_file.close()
	
	def test_positive_client_start(self):
		# start client empty get
		current_time = self.get_current_time()
		self.lock.acquire()
		server_process = self.si.start_server_process(self.lock, current_time, "--port=80")
		time.sleep(5)
		with open("./out/server_out_" + str(current_time) + ".txt", 'r') as server_out_file:
			server_out = server_out_file.readlines()
			assert server_out == ['The server is waiting for requests\n']
			server_out_file.close()
		client_process = self.ci.start_client_process(self.lock, current_time, "get")
		time.sleep(5)
		with open("./out/client_out_" + str(current_time) + ".txt", 'r') as client_out_file:
			client_out = client_out_file.readline()
			assert client_out == "[done]\n"
			client_out_file.close()
		self.si.stop_server(server_process)

if __name__ == '__main__':
	t = Tester()
	t.test_negative_client_start()
	t.test_negative_server_start()
	t.test_positive_client_start()
	# and so on...
	print("Passed")
