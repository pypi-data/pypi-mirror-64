from __future__		import annotations
from typing 		import List
from curses.textpad import rectangle
from jivi.util 		import random_el,Thread,index_random
from jivi.Curses 	import COLOR,CURSES,InputChar,Position,CursesWrapper
import curses
from time import sleep

GHOST_BLOCK = bytes((178,)).decode('cp437')
GHOST_BLOCK = GHOST_BLOCK + GHOST_BLOCK
FREE_SPOT = -1
GHOST_SPOT = -2


LINE_SCORE = [0,5,10,15,100]
LEVEL_SCORE = [0,100,200,500,1000,2000,10000,30000,50000,100000]

def __get_level_scores_till_100():
	retval = []
	FINAL_LEVEL_SCORE = LEVEL_SCORE[-1]
	LEVEL_SCORE_NOW = 0
	for i in range(100):
		if i < len(LEVEL_SCORE):
			LEVEL_SCORE_NOW += LEVEL_SCORE[i]
		else:
			LEVEL_SCORE_NOW += FINAL_LEVEL_SCORE
		retval.append(LEVEL_SCORE_NOW)
	return retval

SCORE_AT_LEVEL = __get_level_scores_till_100()

class Shapes:
	ZShape     = [[0,-1],[0,0],[-1,0],[-1,1]]
	SShape     = [[0,-1],[0,0],[1,0],[1,1]]
	IShape     = [[0,-1],[0,0],[0,1],[0,2]]
	TShape     = [[-1,0],[0,0],[1,0],[0,1]]
	Square     = [[0,0],[1,0],[0,1],[1,1]]
	LShape     = [[-1,-1],[0,-1],[0,0],[0,1]]
	JShape     = [[1,-1],[0,-1],[0,0],[0,1]]
	ALL        = [ZShape,SShape,IShape,TShape,Square,LShape,JShape] 

	@classmethod
	def random(cls):
		i = index_random(cls.ALL)
		return COLOR.B.ALL[i],cls.ALL[i]
class Element:
	curs          : CursesWrapper   = None
	@property
	def total_width(self) -> int:
		return self.offset_x + self.width
	
	@property
	def total_height(self) -> int:
		return self.offset_y + self.height
	
	@property
	def win(self) -> curses.window:
		return self.curs.win

def line_is_done(ar):
	for x in ar:
		if x == FREE_SPOT:
			return False
	return True

class Block:
	shape_index : int       = None
	y           : int       = 1
	x           : int       = 5
	box         : Box       = None
	shape       : List[int] = None
	def __init__(self,box:Box=None,shape_index:int=None,shape:List[int]=None,x:int=5,y:int=1):
		self.x 				= x
		self.y 				= y
		self.box 			= box
		self.shape_index 	= shape_index 	if shape_index is not None 		else index_random(Shapes.ALL)
		self.shape 			= shape 		if shape is not None			else Shapes.ALL[self.shape_index]
		self.grounded		= False





	def can_move(self,x,y,shape=None):
		return self.box.free_pos_shape(x,y,self.shape if shape is None else shape)

	def move(self,x=None,y=None,rotate=None,rotate_inverse=None):
		if x:
			if self.can_move(self.x+x,self.y):
				self.x = self.x+x
				self.box.draw()
				return True
		elif y:
			target_y = self.y + y
			while self.y != target_y:
				if self.can_move(self.x,self.y+1):
					self.y   += 1
				else:
					return self.box.set_new_block(self)
			self.box.draw()
		elif rotate or rotate_inverse:
			new_shape = [[a[1],-a[0]][:] for a in self.shape] if rotate else [[-a[1],a[0]][:] for a in self.shape]
			for x_delta in [0,-1,-2,1,2]:
				new_x = self.x + x_delta
				if self.can_move(new_x,self.y,new_shape):
					self.shape = new_shape
					self.x = new_x
					self.box.draw()
					return
	
	@property
	def ghost_positions(self):
		def gety():
			ghost_y  = self.y
			while True:
				if self.can_move(self.x,ghost_y+1):
					ghost_y += 1
				else:
					return ghost_y
		ghost_y = gety()
		return [[self.x + x,ghost_y + y] for x,y in self.shape]
	
	@property
	def positions(self):
		return [[self.x + x,self.y + y] for x,y in self.shape]

	@property
	def color_dict(self,show_ghost=True):
		retval = dict()
		if show_ghost:
			for x,y in self.ghost_positions:
				if not y in retval:
					retval[y] = dict()
				retval[y][x] = GHOST_SPOT
		for x,y in self.positions:
			if not y in retval:
				retval[y] = dict()
			retval[y][x] = self.shape_index
		return retval
	
	@property
	def color(self):
		return COLOR.B.ALL[self.shape_index]

class Box(Element):
	block         : Block            = None
	lines         : List[List[int]] = []
	old_color     : List[List[int]] = []
	offset_x      : int              = 1
	offset_y      : int              = 0
	height        : int              = 20
	block_per_row : int              = 10
	curs          : CursesWrapper   = None

	def __init__(self,curs:Tetris=None,offset_x=None,offset_y=None,block_per_row=None,height=None,show_ghost=True):
		self.__event_line_scored_listeners 	= []
		self.curs   						= curs
		self.offset_x 						= offset_x 		if offset_x			is not None else self.offset_x
		self.offset_y 						= offset_y 		if offset_y			is not None else self.offset_y
		self.block_per_row					= block_per_row if block_per_row 	is not None else self.block_per_row
		self.height							= height		if height			is not None else self.height
		self.lines  						= [[-1 for x in range(self.block_per_row)] for y in range(self.height)]
		self.show_ghost						= show_ghost
		self.draw_static()
		self.set_new_block()
		self.register_keys()
		self.draw()

	def event_line_scored_register(self,func):
		self.__event_line_scored_listeners.append(func)
	
	def set_new_block(self,block:Block=None):
		if block:
			for x,y in block.positions:
				self.lines[y][x] = block.shape_index

		new_lines = []
		for l in self.lines:
			if not line_is_done(l):
				new_lines.append(l)
		
		lines_scored = len(self.lines) - len(new_lines)
		if lines_scored:
			
			for f in self.__event_line_scored_listeners:
				f(lines_scored)
			
			new_lines = [[-1 for x in range(self.block_per_row)] for y in range(lines_scored)] + new_lines
			self.lines = new_lines
		
		self.block = Block(box=self)
		self.draw()
	
	def draw_static(self):
		rectangle(self.win,0,0,1+self.height,self.offset_x+self.width)
	
	def draw_old(self):
		color_conv = dict()
		color_conv[-1] = COLOR.B.BLACK
		color_conv[-2] = COLOR.B.MAGENTA

		block_color_dict = self.block.color_ghost_dict if self.show_ghost else dict
		for y,t in self.block.color_dict.items():
			for x,color in t.items():
				block_color_dict[y][x] = color
			
		new_color = []
		for y,color_ar in enumerate(self.lines):
			block_row_dict = block_color_dict.get(y,dict())
			for x,color in enumerate(color_ar):
				color_value = block_row_dict.get(x,color)
				if color_value in color_conv:
					color_value = color_conv[color_value]
				new_color.append([y,x,color_value])

		if self.old_color:
			differences = []
			for i in range(len(new_color)):
				if new_color[i][2] != self.old_color[i][2]:
					differences.append(new_color[i])
		else:
			differences = new_color

		for y,x,color in differences:
			self.win.addstr(y+1,x*2+self.offset_x,"  ",color)
	
	def draw(self):
		color_conv = dict()
		color_conv[-1] = COLOR.B.BLACK   #EMPTY
		color_conv[-2] = COLOR.B.MAGENTA #GHOST
		char_conv = dict()
		char_conv[-1] = "  "
		char_conv[-2] = GHOST_BLOCK
		for i,c in enumerate(COLOR.B.ALL):
			char_conv[i] = "  "
			color_conv[i] = c
		

		block_color_dict = self.block.color_dict

		new_color = []
		for y,color_ar in enumerate(self.lines):
			block_row_dict = block_color_dict.get(y,dict())
			for x,block_type_index in enumerate(color_ar):
				block_type_index = block_row_dict.get(x,block_type_index)
				new_color.append([y,x,block_type_index])

		if self.old_color:
			differences = []
			for i in range(len(new_color)):
				if new_color[i][2] != self.old_color[i][2]:
					differences.append(new_color[i])
		else:
			differences = new_color

		for y,x,block_type_index in differences:
	
			a = char_conv[block_type_index]
			b = color_conv[block_type_index]
			self.win.addstr(y+1,x*2+self.offset_x,char_conv[block_type_index],color_conv[block_type_index])


		self.win.refresh()


	def free_pos_shape(self,x:int,y:int,shape:List[List[int]]):
		for x_shape,y_shape in shape:
			X,Y = x+x_shape,y+y_shape
			if ((X < 0 or X >= self.block_per_row) or (Y < 0 or Y >= self.height) or (self.lines[Y][X] != FREE_SPOT)):
				return False
		return True
	
	def register_keys(self):
		def key(key,func,*a,no_arg_default=True,**b):
			b["no_arg_default"] 	= no_arg_default
			self.curs.on_key(key,func,**b)
		key('space',self.block_move,kwargs=dict(y=100))
		key('down',self.block_move,kwargs=dict(y=1))
		key('right',self.block_move,kwargs=dict(x=1))
		key('left',self.block_move,kwargs=dict(x=-1))
		key('up',self.block_move,kwargs=dict(rotate_inverse=True))

	def block_move(self,x=None,y=None,rotate=None,rotate_inverse=None):
		self.block.move(x=x,y=y,rotate=rotate,rotate_inverse=rotate_inverse)

	@property
	def width(self) -> int:
		return self.block_per_row*2

class Score(Element):
	curs     : CursesWrapper = None
	offset_x : int           = 1
	offset_y : int           = 0
	width    : int           = 20
	height   : int           = 5
	__level  : int           = 0
	__score  : int           = 0
	__lines  : int           = 0
	

	@property
	def time_interval(self):
		return 1

	@property
	def score(self):
		return self.__score
	
	@score.setter
	def score(self,value):
		self.__score = value

		next_level = self.level
		while value > SCORE_AT_LEVEL[next_level+1]:
			next_level += 1
		
		if next_level != self.level:
			self.level = next_level
	
	@property
	def level(self):
		return self.__level
	@level.setter
	def level(self,value):
		self.__level = value
		self.draw()
	
	@property
	def lines(self):
		return self.__lines
	@lines.setter
	def lines(self,value):
		to_add_value = value - self.__lines
		self.__lines = value
		self.score += LINE_SCORE[to_add_value]
		self.draw()

	def __init__(self,curs:CursesWrapper=None,offset_x=None,offset_y=None,height=None,width=None,score=0,level=0,lines=0):
		self.curs   		= curs
		self.offset_x 		= offset_x 		if offset_x			is not None else self.offset_x
		self.offset_y 		= offset_y 		if offset_y			is not None else self.offset_y
		self.width			= width 		if width		 	is not None else self.width
		self.height			= height		if height			is not None else self.height
		self.__level 		= level
		self.__score		= score
		self.__lines		= lines
		self.draw_static()
	
	def draw_static(self):
		def add(y,x,s):
			self.win.addstr(self.offset_y+y,self.offset_x+x,s,COLOR.F.WHITE)

		rectangle(self.win,self.offset_y,self.offset_x,self.offset_y+self.height,self.offset_x+self.width)
		add(1,1,"Level")
		add(2,1,"Lines")
		add(3,1,"Score")
	
	def draw(self):
		end_x = self.offset_x + self.width
		def add(y,n):
			s  = str(n)
			sl = len(s)
			x  = end_x-sl
			self.win.addstr(self.offset_y+y,x,s,COLOR.F.WHITE)
		add(1,self.level)
		add(2,self.lines)
		add(3,self.score)

	def line_scored(self,amount):
		self.lines += amount

class Tetris(CursesWrapper):
	score      : Score = None
	show_lines : bool  = False
	show_ghost : bool  = False
	box        : Box   = None
	def __init__(self,show_lines=False,show_ghost=True):
		super().__init__()
		self.show_lines = show_lines
		self.show_ghost = show_ghost
		curses.wrapper(self.initscr)

	def initscr(self,win:curses.window):
		super().initscr(win)
		on_key     = self.on_key
		@on_key('esc')
		def f(m:Tetris):
			m.stop()
		
		self.box   = Box(curs=self,show_ghost=self.show_ghost)
		self.score = Score(curs=self,offset_x=self.box.total_width+1)
		self.box.event_line_scored_register(self.score.line_scored)
		self.key_reader()

if __name__ == "__main__":
	Tetris(show_lines=False)