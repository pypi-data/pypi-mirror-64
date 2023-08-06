from __future__ 			import annotations
from .base import BaseView as B
from typing import List


class Tetris(B.Tetris):
	def init(self):
		self.nextBlock    = B.NextBlock()
		self.holdingBlock = B.HoldingBlock()
		self.box          = B.Box()
		self.score        = B.Score()
	
	def start(self):
		pass