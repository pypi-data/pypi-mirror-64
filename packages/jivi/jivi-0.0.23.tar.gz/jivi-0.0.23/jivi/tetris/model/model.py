import traceback
from time import sleep, time
from typing import List

from ..constant import TetrisCtrlEvent,DisplayData
from jivi.thread import Thread

from ..controller import CtrlElement
from ..controller import Tetris as Controller
from ..view import View




class Tetris:
	ctrlTrg = TetrisCtrlEvent
	view : View
	ctrl : Controller
	dispData : DisplayData
	def __init__(self,viewClass:View):
		self.ctrl = Controller()

		self.dispData = DisplayData({k : v.get_data for k,v in self.ctrl.elements.items()})
		self.view = viewClass(self.dispData)
		self._running_index = 0
		self.register_listeners()
		

	def start(self):
		self.view.start()
		self.running = True
		self._running_index += 1
		def thread_condition(running_index):
			return self.running and self._running_index == running_index
		
		def thread_first_run(*a,**b):
			self.next_auto_drop = time() + self.ctrl.time_interval
		@Thread.register(options=Thread.options(interval=0.1,condition=thread_condition,first_run=thread_first_run),args=[self._running_index])
		def tick_thread(running_index):
			if time() > self.next_auto_drop:
				self.ctrl.box.move(y=1)
				self.next_auto_drop = time() + self.ctrl.time_interval

			self.dispData.lastChanged = {k : v.last_change for k,v in self.ctrl.elements.items()}

			self.view.check_changes()
			


		while self.running:
			sleep(0.1)
		self._running_index += 1
	def register_listeners(self):
		cBox = self.ctrl.box
		c = self.ctrlTrg
		@c.do_exit()
		def f(ev):
			self.exit()

		@c.left()
		def f(ev):
			cBox.move(x=-1)
		
		@c.right()
		def f(ev):
			cBox.move(x=+1)
		
		@c.down()
		def f(ev):
			cBox.move(y=1)
		
		@c.up()
		def f(ev):
			cBox.move(rotate=1)
		
		@c.holding()
		def f(ev):
			self.ctrl.box.switch_holding()
		
		@c.drop()
		def f(ev):
			cBox.move(drop_down=True)
		
	def exit(self):
		self._running_index += 1
		self.running = False
		self.view.exit()
		Thread.stop_all()
