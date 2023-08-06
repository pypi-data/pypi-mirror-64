from __future__ 			import annotations
from .base import BaseView as B
from typing import List
from ..constant import CLine,GHOST_BLOCK_CHAR,ALL_SHAPES,Data
from jivi.Curses import COLOR,get_keyname,valid_key,rectangle,curses
from jivi.event import EventWithKey,Event

from time import time
from jivi.thread import Thread

def curses_get_window() -> curses.window:
	win = curses.initscr()
	curses.start_color()
	curses.mousemask(1)
	curses.curs_set(0)
	win.keypad(1)
	curses.mouseinterval(50)
	COLOR.init()
	return win

class ViewElement(B.ViewElement):
	offset_x : int
	offset_y : int
	width    : int
	height   : int
	win      : curses.window

	def __init__(self,win:curses.window,offset_x=None,offset_y=None,height=None,width=None):
		self.win 			= win
		self.offset_x 		= offset_x 		if offset_x			is not None else self.offset_x
		self.offset_y 		= offset_y 		if offset_y			is not None else self.offset_y
		self.width			= width 		if width		 	is not None else self.width
		self.height			= height		if height			is not None else self.height
		super().__init__()
		self.draw_static()
	

	def draw_static(self):
		self._draw_rec()

	@property
	def total_width(self) -> int:
		return self.offset_x + self.width
	
	@property
	def total_height(self) -> int:
		return self.offset_y + self.height
	

	def draw(self,y,x,txt,attr=None):
		self.win.addstr(self.offset_y+y,self.offset_x+x,txt,attr)

	def refresh(self):
		y,x = self.win.getmaxyx()
		
		self.win.move(y-1,x-1)
		self.win.refresh()
		self.last_update = time()

	def _draw_rec(self):
		rectangle(self.win,self.offset_y,self.offset_x,self.offset_y+self.height,self.offset_x+self.width)

class Score(B.Score,ViewElement):
	offset_x      : int = 23
	offset_y      : int = 0
	width         : int = 23
	height        : int = 5

	
	def draw_static(self):
		def add(y,x,s):
			self.draw(y,x,s,COLOR.F.WHITE)
		self._draw_rec()
		
		add(1,1,"Level")
		add(2,1,"Lines")
		add(3,1,"Score")

	def _draw_dynamic(self,data:Data.Score):
		end_x = self.offset_x + self.width
		def add(y,n):
			s  = str(n)
			sl = len(s)
			x  = end_x-sl
			self.win.addstr(self.offset_y+y,x,s,COLOR.F.WHITE)
		add(1,data.level)
		add(2,data.lines)
		add(3,data.score)

		self.refresh()

class Box(B.Box,ViewElement):
	offset_x : int = 1
	offset_y : int = 0
	height   : int = 21
	width    : int = 21
	char           = dict()
	color          = dict()

	def init(self):
		self.char  = dict()
		self.color = dict()
		def s(n:int,color=None,char=" "):
			self.char[n]  = char + char
			self.color[n] = COLOR.B.ALL[n] if color is None else color
		s(CLine.empty,color=COLOR.B.BLACK)
		s(CLine.ghost,color=COLOR.B.MAGENTA,char=GHOST_BLOCK_CHAR)
		for index in range(len(ALL_SHAPES)):
			s(index)
	

	def _draw_diferences(self,difference,data:Data.Box):
		for x,y,type_block in difference:
			self.draw(y+1,1+x*2,self.char[type_block],self.color[type_block])

		self.refresh()







class BlockContainer(ViewElement):
	title : str = ""
	width    : int = 11
	height   : int = 5
	def _draw_dynamic(self,data:Data.BlockContainer):
		for y in range(self.height - 2):
			self.draw(y+1,1," "*(self.width - 2),COLOR.B.BLACK)
		
		if data.shape_type is not None:
			for x,y in ALL_SHAPES[data.shape_type][0]:
				self.draw(y+2,x*2+6,"  ",COLOR.B.ALL[data.shape_type])
		self.refresh()
	
	def draw_static(self):
		self.draw(-1,1,self.title,COLOR.F.WHITE)
		self._draw_rec()
	
class HoldingBlock(B.HoldingBlock,BlockContainer):
	title          = "Holding"
	offset_x : int = 35
	offset_y : int = 7

class NextBlock(B.NextBlock,BlockContainer):
	offset_x : int = 23
	offset_y : int = 7
	title          = "Next"

class Tetris(B.Tetris):



	def init(self):
		self.win          = curses_get_window()
		self.on_key       = EventWithKey(valid_key=valid_key,format_key=get_keyname)
		self.nextBlock    = NextBlock(self.win)
		self.holdingBlock = HoldingBlock(self.win)
		self.box          = Box(self.win)
		self.score        = Score(self.win)
		self.running      = False
		self._register_ev()
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




	def check_changes(self):
		for k,v in self.elements.items():
			if self.dispData.lastChanged[k] > v.last_update:
				v.draw_dynamic(self.dispData.getData[k](),self.dispData.lastChanged[k])

	def start(self):
		self.running = True
		@Thread.register(options=Thread.options(condition=Thread.conditionProp(self,'running')))
		def read_char_thread():
			x = self.win.getch()
			if x > 0:
				self.on_key.fire(x)
		


	def exit(self):
		self.running = False
		curses.endwin()
	
