from __future__ 			import annotations
from typing import List
from ..constant import CLine,GHOST_BLOCK_CHAR,ALL_SHAPES,Data
from jivi.Curses import COLOR,get_keyname,valid_key,rectangle,curses
from jivi.event import EventWithKey
from ..constant import TetrisCtrlEvent,DisplayData
from time import time
from jivi.thread import Thread


class ViewElement:
	def __init__(self):
		self.init()
		self.last_update = 0

	def init(self):
		pass

	def _draw_dynamic(self,data):
		pass

	def draw_dynamic(self,data,last_update):
		self.last_update = last_update
		self._draw_dynamic(data)
	


class HoldingBlock(ViewElement):
	dataType = Data.BlockContainer



class NextBlock(ViewElement):
	dataType = Data.BlockContainer


class Score(ViewElement):
	dataType = Data.Score

class Box(ViewElement):
	last_lines = None
	def _draw_dynamic(self,data:Data.Box):
		BLOCK_TYPE_INDEX = 2

		def get_diference():
			if not self.last_lines:
				for a in data.lines:
					yield a
			else:
				for index in range(len(data.lines)):
					if self.last_lines[index][BLOCK_TYPE_INDEX] != data.lines[index][BLOCK_TYPE_INDEX]:
						yield data.lines[index]

			self.last_lines = data.lines
		
		self._draw_diferences(get_diference(),data)

	def _draw_diferences(self,difference,data:Data.Box):
		pass

	




class Tetris:
	ctrlTrg = TetrisCtrlEvent
	nextBlock    : NextBlock   
	holdingBlock : HoldingBlock
	box     : Box         
	score   : Score       
	def __init__(self,dispData:DisplayData):
		self.running = False
		self.dispData = dispData
		self.init()

	def init(self):
		pass
	def check_changes(self):
		pass

	@property
	def elements(self):
		return dict(box=self.box,score=self.score,nextBlock=self.nextBlock,holdingBlock=self.holdingBlock)
class BaseView:
	Tetris       = Tetris
	Score        = Score
	NextBlock    = NextBlock
	HoldingBlock = HoldingBlock
	Box          = Box
	ViewElement  = ViewElement