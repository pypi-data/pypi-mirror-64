from __future__ 			import annotations
from .base import BaseView as B
from typing import List
from ...tcpsock import TCPClient,TCPServer
import json
from ...event import EventWithKey
from ...Curses import valid_key,get_keyname

server_port = 4124
client_port = 4123

class Tetris(B.Tetris):
	def init(self):
		self.nextBlock    = B.NextBlock()
		self.holdingBlock = B.HoldingBlock()
		self.box          = B.Box()
		self.score        = B.Score()
		self.on_key       = EventWithKey(valid_key=valid_key,format_key=get_keyname)
		self._register_ev()
	def on_receive(self,data:dict):
		if key_press := data.get("key",None):
			self.on_key.fire(key_press)
			return
		
	
	def _register_ev(self):
		ok = self.on_key.register
		mapper = dict(
			esc=self.ctrlTrg.do_exit,
			left=self.ctrlTrg.left,
			right=self.ctrlTrg.right,
			down=self.ctrlTrg.down,
			up=self.ctrlTrg.up,
			dc=self.ctrlTrg.holding,
			space=self.ctrlTrg.drop)
			
		for k,v in mapper.items():
			self.on_key.register(k,self.on_key.cb(clear_args=True),func=v.fire)


	def start(self):
		self.server = TCPServer(port=server_port,cb=self.on_receive,decode="utf8",is_json=True)
		
	def send(self,msg):
		if isinstance(msg,dict):
			msg = json.dumps(msg)
		TCPClient.send(client_port,msg=msg)
	
	def check_changes(self):
		has_changed = False
		for k,v in self.elements.items():
			if self.dispData.lastChanged[k] > v.last_update:
				v.last_update = self.dispData.lastChanged[k]
				has_changed = True
			
		if has_changed:
			self.send({k : v().to_dict() for k,v in self.dispData.getData.items()})


	def exit(self):
		self.send(dict(electron_command="exit"))
		self.running = False
		self.server.shutdown()
		