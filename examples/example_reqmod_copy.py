# -*- coding: utf8 -*-

import random
import SocketServer

from icapserver import *

class ThreadingSimpleServer(SocketServer.ThreadingMixIn, ICAPServer):
	pass

class ICAPHandler(BaseICAPRequestHandler):

	def example_OPTIONS(self):
		self.set_icap_response(200)
		self.set_icap_header('Methods', 'REQMOD')
		self.set_icap_header('Service', 'ICAP Server 1.0')
		self.set_icap_header('Options-TTL', '3600')
		self.set_icap_header('Preview', '0')
		self.send_headers(False)

	def example_REQMOD(self):
		self.set_icap_response(200)

		self.set_enc_request(' '.join(self.enc_req))
		for h in self.enc_req_headers:
			for v in self.enc_req_headers[h]:
				self.set_enc_header(h, v)

		if not self.has_body:
			self.send_headers(False)
			return
		if self.preview:
			prevbuf = ''
			while True:
				chunk = self.read_chunk()
				if chunk == '':
					break
				prevbuf += chunk
			if self.ieof:
				self.send_headers(True)
				if len(prevbuf) > 0:
					self.write_chunk(prevbuf)
				self.write_chunk('')
				return
			self.cont()
			self.send_headers(True)
			if len(prevbuf) > 0:
				self.write_chunk(prevbuf)
			while True:
				chunk = self.read_chunk()
				self.write_chunk(chunk)
				if chunk == '':
					break
		else:
			self.send_headers(True)
			while True:
				chunk = self.read_chunk()
				self.write_chunk(chunk)
				if chunk == '':
					break

	def example_RESPMOD(self):
		self.no_adaptation_required()

port = 13440

server = ThreadingSimpleServer(('', port), ICAPHandler)
try:
	while 1:
		server.handle_request()
except KeyboardInterrupt:
	print "Finished"
