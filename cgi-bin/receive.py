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
		if len(queues[queue]) < 100:
			queues[queue].append(message)
	elif not queues.get(queue):
		queues[queue] = [message]

		
	with open('queues.srlz', 'wb') as f:
		pickle.dump(queues, f)

print("[done]")


#print("Hello! Perhaps you are using POST method.")
#print("Your message is %s. And you queue is %s" % (message, queue))