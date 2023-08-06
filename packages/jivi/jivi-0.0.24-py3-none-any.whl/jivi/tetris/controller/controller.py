from jivi.event import EventWithKeyWithParent
from typing import List
import random,traceback,math
from ..constant import ALL_SHAPES,CLine,ScoreSetting,Data
from itertools import product
from time import time

def get_random_shape_index():
	return random.randint(0,len(ALL_SHAPES) - 1)

def ar_passes_all(condition,ar=None,as_function=False,inverse=False):
	if as_function:
		def ret_val(ar):
			return ar_passes_all(condition,ar=ar,inverse=inverse)
		return ret_val
	if inverse:
		return not ar_passes_all(condition,ar=ar)
	for x in ar:
		if not condition(x):
			return False
	return True

class Block:
	def __init__(self,x:int,y:int,shape_index:int=None,rotation:int=0):
		self.x           = x
		self.y           = y
		self.shape_index = get_random_shape_index if shape_index is None else shape_index
		self.set_rotation(rotation)
	def set_rotation(self,rotation):	self.__rotation = rotation % 4
	def get_positions(self):			return [[x+self.x,y+self.y] for x,y in ALL_SHAPES[self.shape_index][self.__rotation]]
	def move(self,x=0,y=0,rotate=0): 	return self.__class__(shape_index=self.shape_index,x=self.x + x,y=self.y + y,rotation=self.__rotation + rotate)
	def __repr__(self):					return f'{self.__class__.__name__} ({self.x},{self.y})'



class CtrlElement:
	last_change : int = 0
	def __init__(self):
		self.changed()
	
	def changed(self):
		self.last_change = time()


	def get_data(self):
		pass

class Score(CtrlElement):
	def __init__(self):
		self.score       = 0
		self.lines       = 0
		self.level       = 0
		super().__init__()
	def _update_level(self):
		while self.score > ScoreSetting.score_at_level[self.level]:
			self.level += 1
	
	def add_lines(self,to_add:int):
	
		self.lines += to_add
		self.score += ScoreSetting.score_for_lines_made[to_add]
		self._update_level()
		self.last_change = time()

	def get_data(self) -> Data.Score:
		return Data.Score(level=self.level,score=self.score,lines=self.lines)


class BlockContainer(CtrlElement):
	_shape : int = -1
	@property
	def shape(self):
		return self._shape
	
	@shape.setter
	def shape(self,n):
		self._shape = n
		self.changed()
	
	def get_data(self) -> Data.BlockContainer:
		if self._shape == -1:
			return Data.BlockContainer()
		return Data.BlockContainer(shape_type=self._shape)
	
	@property
	def empty(self):
		return self.shape == -1
	
	def set_random_shape(self):
		self.shape = get_random_shape_index()
	

class Box(CtrlElement):
	def __init__(self,height:int,width:int,add_lines:callable):
		self.height 				= height
		self.width  				= width
		self.lines 					= [[CLine.empty for col in range(width)] for l in range(height)]
		self.add_lines 				= add_lines
		self.nextBlock				= BlockContainer()
		self.holdingBlock			= BlockContainer()
		self._can_switch_holding 	= False
		self.nextBlock.set_random_shape()
		super().__init__()
		self.create_new_block()

	def switch_holding(self):
		if not (self.block and self._can_switch_holding):
			return
		
		def get_valid_block(nb:Block):
			for r in [0,1,2,3]:
				for x in [0,-1,1,-2,2]:
					test_block = nb.move(x=x,rotate=r)
					if self.valid_block(test_block):
						return test_block

			return False
		
		nb             : Block = self.block.move()
		nb.shape_index         = get_random_shape_index() if self.holdingBlock.empty else self.holdingBlock.shape
		nb                     = get_valid_block(nb)

		if not nb:
			return
		
		self.holdingBlock.shape = self.block.shape_index
		self.block = nb
		self.changed()
		self._can_switch_holding = False


	def valid_block(self,b:Block):
		for x,y in b.get_positions():
			if not ( (0 <= x < self.width) and (0 <= y < self.height) and (self.lines[y][x] == CLine.empty) ):
				return False
		return True
	
	def get_data(self) -> Data.Box:
		tmp_val = [l[:] for l in self.lines]
		def update(b):
			def get_ghost() -> Block:
				ret_block 	= b.move()
				new_block 	= ret_block.move(y=1)
				while self.valid_block(new_block):
					ret_block = new_block
					new_block = new_block.move(y=1)
				return ret_block
			ghost_block = get_ghost()
			for x,y in ghost_block.get_positions():
				tmp_val[y][x] = CLine.ghost
			for x,y in b.get_positions():
				tmp_val[y][x] = b.shape_index

		shape_index = None
		if self.block:
			shape_index = self.block.shape_index
			update(self.block.move())
		return Data.Box(lines=[[x,y,tmp_val[y][x]] for y,x in product(range(self.height),range(self.width))],shape_type=shape_index)
	
	def create_new_block(self):
		
		b                    = Block(x=math.floor(self.width/2),y=0,shape_index=self.nextBlock.shape)
		if self.valid_block(b):
			self.nextBlock.set_random_shape()
			self.block               = b
			self._can_switch_holding = True
			
		else:

			self.block     = None
			self.game_over = True

		self.changed()
	def new_block(self,b:Block=None,trying_to_move=False):
		if b is None:
			b = Block(x=math.floor(self.width/2),y=0)
		
		if self.valid_block(b):
			self.block = b
			if not trying_to_move:
				self._can_switch_holding = True
			self.changed()
			return b
		
		if trying_to_move:
			return False
		
		self.block     = None
		self.game_over = True
		self.changed()


	def move(self,x=0,y=0,rotate=0,drop_down=False):
		if not self.block:	
			return
		
		def block_dropped():
			for x,y in self.block.get_positions():
				self.lines[y][x] = self.block.shape_index
			new_lines		= list(filter(ar_passes_all(lambda x : x >= 0,as_function=True,inverse=True),self.lines))
			lines_scored 	= len(self.lines) - len(new_lines)
			if lines_scored:
				self.lines = [[CLine.empty for x in range(self.width)] for y in range(lines_scored)] + new_lines
				self.add_lines(lines_scored)

			
			self.create_new_block()
		
		def move_and_set_if_valid(x=0,y=0,rotate=0,ar=[],failed_cb=None,repeat=False):
			ar = [dict(x=x,y=y,rotate=rotate)] if not ar else ar
			def try_ar():
				for t in ar:
					if self.new_block(self.block.move(**t),trying_to_move=True):
						return True
				return False
			
			while try_ar():
				if not repeat:
					return
			
			if failed_cb: 
				failed_cb()
			
		
		if x: 			return move_and_set_if_valid(x=x)
		if y: 			return move_and_set_if_valid(y=y,failed_cb=block_dropped)
		if rotate: 		return move_and_set_if_valid(ar=[dict(x=x,rotate=rotate) for x in [0,-1,1,-2,2]])
		if drop_down: 	return move_and_set_if_valid(y=1,failed_cb=block_dropped,repeat=True)

class Tetris:
	def __init__(self):
		self.height			= 20
		self.width			= 10
		self.score     		= Score()
		self.box    		= Box(self.height,self.width,add_lines=self.score.add_lines)
	


	@property
	def elements(self):
		return dict(box=self.box,score=self.score,nextBlock=self.nextBlock,holdingBlock=self.holdingBlock)
	@property
	def nextBlock(self):
		return self.box.nextBlock

	


	@property
	def holdingBlock(self):
		return self.box.holdingBlock

	


		
		
	@property
	def time_interval(self):
		return ScoreSetting.time_interval_at_level[self.score.level]
	