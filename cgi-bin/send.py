#!/usr/bin/env python3

import cgi, cgitb
import pickle

form = cgi.FieldStorage()
message = form.getvalue('message')
queue = form.getvalue('queue')
queues = {}
print("Content-type: text")
print()
if int(queue) >= 0 and int(queue) <= 10000:
	with open('queues.srlz', 'rb') as f:
		queues = pickle.load(f)

	if queues.get(queue):
		print(queues[queue].pop(0))
	elif not queues.get(queue):
		queues.pop(queue, None)
		
	with open('queues.srlz', 'wb') as f:
		pickle.dump(queues, f)

print("[done]")
	
#print("Hello! Perhaps you are using GET method.")
#print("Your message is %s. And you queue is %s" % (message, queue))
