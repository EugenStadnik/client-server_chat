#!/usr/bin/env python3

import sys
import argparse

class ParamParser:
	
	def __init__(self, modul_version):
		self.modul_version = modul_version
	
	def parse_server_param(self):
		parser = argparse.ArgumentParser(
            description = '''This is a primitive server implemented as a hiring task solvation. Used to receive and store text messages internally in queues and send them back to clients upon request. It has up to 10000 queues. The default queue value is  '0' It may ignor the message, if the target queue has more than 100 messages. The oldest message is returned to client and deleted afterwards. If there is no message in the queue, server may ignore the request''',
            epilog = '''(c) Yevhen Stadnik 2017. The author of thiss app, as usual, has no responsibility about anything.'''
		)
		parser.add_argument('--port', metavar='N', required=True, type=int, help='This is mandatory option. Use integer in the range 0...65535.')
		
		parser.add_argument ('--version',
			action='version',
			help = 'Show version',
			version='%(prog)s {}'.format (self.modul_version))
		
		return parser
	
	def parse_client_param(self):
		
		parser = argparse.ArgumentParser(
			description = '''This is a primitive client implemented as a hiring task solvation. This application is used to send text messages to server and print text messages retrieved from the server using command line. The \'server.py\' should ran first.''',
			epilog = '''(c) Yevhen Stadnik 2017. The author of thiss app, as usual, has no responsibility about anything.''',
			add_help = False
		)
		
		subparsers = parser.add_subparsers (
			dest = 'command', title = 'Posible args',
			description = 'Args that should be as a first parameter of %(prog)s. For more information use \'post -h\' or \'get -h\' option.'
		)
		
		post_parser = subparsers.add_parser ('post', add_help = False,
			help = 'Start the %(prog)s in the \'post\' mode.',
			description = '''Start the %(prog)s in the \'post\' mode. In this mode the programm posts message \'--message\' in a queue \'--queue\' on server \'server.py\'. The \'server.py\' should ran first.''',
			epilog = '''(c) Yevhen Stadnik 2017. The author of thiss app, as usual, has no responsibility about anything.'''
		)
		post_group = post_parser.add_argument_group (title='Parameters')
		post_group.add_argument ('--message', metavar='<message>', required=True, help='This option is mandatory only via post method. It shouldn\'t be empty.')
		post_group.add_argument ('--queue', metavar='N', nargs='?', default=0, help='This parameter is optional. Use integer in the range 0...10000. Default value is 0. If the value is out of range - the request will be ignored.')
		post_group.add_argument ('--help', '-h', action='help', help='Help')
		
		get_parser = subparsers.add_parser ('get', add_help = False,
			help = 'Start the %(prog)s in the \'get\' mode',
			description = '''Start the %(prog)s in the \'get\' mode. In this mode the programm receives message the oldest message in a queue \'--queue\' from server \'server.py\'. The \'server.py\' should ran first.''',
			epilog = '''(c) Yevhen Stadnik 2017. The author of thiss app, as usual, has no responsibility about anything.'''
		)
		get_group = get_parser.add_argument_group (title='Parameters')
		get_group.add_argument ('--queue', metavar='N', nargs='?', default=0, help='This parameter is optional. Use integer in the range 0...10000. Default value is 0. If the value is out of range - the request will be ignored.')
		get_group.add_argument ('--help', '-h', action='help', help='Help')
			
		parent_group = parser.add_argument_group (title='Parameters')
		parent_group.add_argument ('--help', '-h', action='help', help='Help')
		parent_group.add_argument ('--version',
			action='version',
			help = 'Show version',
			version='%(prog)s {}'.format (self.modul_version))
		
		return parser