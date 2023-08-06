import socket,traceback
from jivi.thread import Thread
import socketserver
import traceback
import json


class MyTCPHandler(socketserver.BaseRequestHandler):
	def handle(self):
		self.data = self.request.recv(1024).strip()
		print("{} wrote:".format(self.client_address[0]))
		print(self.data)

class TCPServer:
	server : socketserver.TCPServer
	def __init__(self,host:str="localhost",port:int=None,cb:callable=None,decode=None,is_json=False):
		self.host    = host
		self.port    = port
		self.cb      = cb
		self.decode  = decode
		self.is_json = is_json
		self.server  = None
		Thread.register(options=Thread.options(no_loop=True),func=self.create_server)


	def data_handler(self,rawdata):
		data = rawdata
		try:
			if self.decode:
				data = data.decode(self.decode)
			if self.is_json:
				data = json.loads(data)

			self.cb(data)
		except:
			print(traceback.format_exc())
		
	def shutdown(self):
		if self.server:
			self.server.shutdown()
		
	def create_server(self):
		data_handler = self.data_handler
		class MyTCPHandler(socketserver.BaseRequestHandler):
			def handle(self):
				data_handler(self.request.recv(1024).strip())
		with socketserver.TCPServer((self.host, self.port), MyTCPHandler) as server:
			self.server = server
			server.serve_forever()


class TCPClient:
	@staticmethod
	def send(port:int,host:str="localhost",msg:str="No message",cb=None):
		
		try:
			msg_byte = msg.encode()
			s        = socket.socket()
			s.connect((host,port))
			s.send(msg_byte)
			s.close()
			return True
		except:
			#print(traceback.format_exc())
			return False

