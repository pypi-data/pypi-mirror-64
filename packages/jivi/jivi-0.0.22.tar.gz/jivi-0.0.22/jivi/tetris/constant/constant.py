import math
from typing import List
from jivi.event import Event

def get_all_shapes():
	def get_rotations(base_shape):
		def to_pos_ar(ar):
			ret_ar = []
			start_x = 0 - math.ceil(len(ar[0])/2)

			for y,line in enumerate(ar):
				for x,val in enumerate(line):
					if not val:
						continue

					ret_ar.append([x+start_x,y])
			return ret_ar


		def mirrorv(ar):
			h = len(ar)
			w = len(ar[0])
			return [[ar[i][w - 1 - j] for j in range(w)] for i in range(h)]


		def mirrorh(ar):

			h = len(ar)
			w = len(ar[0])
			return [[ar[h - 1 - i][j] for j in range(w)] for i in range(h)]
		
		def transpose(ar):
			h = len(ar)
			w = len(ar[0])
			return [[ar[i][j] for i in range(h)] for j in range(w)]
		ar = [[int(c) for c in l] for l in base_shape]
		
		rotations = []

		for funcar in [[],[transpose,mirrorv],[mirrorh,mirrorv],[transpose,mirrorh]]:
			rotation = ar
			for f in funcar:
				rotation = f(rotation)
			rotations.append(rotation)
	
		return [to_pos_ar(x) for x in rotations]
	ret_val = []
	def a(base_shape):
		ret_val.append(get_rotations(base_shape))

	a([
		"010",
		"111"
	])
	a([
		"011",
		"110"
	])
	a([
		"110",
		"011"
	])
	a([
		"1111"
	])
	a([
		"11",
		"11"
	])
	a([
		"111",
		"100"
	])
	a([
		"100",
		"111"
	])
	return ret_val

ALL_SHAPES = get_all_shapes()




LEVEL_SCORE = [0,100,200,500,1000,2000,10000,30000,50000,100000]

def get_level_scores_till_100():
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

def get_time_interval_at_level_till_100():
	retval = [1,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2]
	retval += [0.2]*(100 - len(retval))
	return retval



class ScoreSetting:
	score_for_lines_made 	= [0,5,10,15,100]
	score_at_level       	= get_level_scores_till_100()
	time_interval_at_level	= get_time_interval_at_level_till_100()


GHOST_BLOCK_CHAR = bytes((178,)).decode('cp437')

class CLine:
	empty = -1
	ghost = -2



	

class Data:
	class Box:
		def __init__(self,lines:List[List[int]],shape_type:int=None):
			self.lines      = lines
			self.shape_type = shape_type

		def to_dict(self):
			return dict(lines=self.lines,shape_type=self.shape_type)
	class Score:
		def __init__(self,level:int=0,score:int=0,lines:int=0):
			self.level = level
			self.score = score
			self.lines = lines
		def to_dict(self):
			return {k : getattr(self,k) for k in 'level,score,lines'.split(',')}
	class BlockContainer:
		def __init__(self,shape_type:int=None):
			self.shape_type = shape_type


		def to_dict(self):
			return dict(shape_type=self.shape_type)


class DisplayData:
	def __init__(self,get_data_dict):
		self.lastChanged = dict(box=0,score=0,nextBlock=0,holdingBlock=0)
		self.getData     = get_data_dict


class TetrisCtrlEventClass:
	do_exit : Event
	left    : Event
	right   : Event
	down    : Event
	up      : Event
	holding : Event
	drop    : Event
	def __init__(self):
		self.do_exit = Event()
		self.left    = Event()
		self.right   = Event()
		self.down    = Event()
		self.up      = Event()
		self.holding = Event()
		self.drop    = Event()

	__singleton = None
	@classmethod
	def get(cls):
		if not cls.__singleton:
			cls.__singleton = cls()
		return cls.__singleton
TetrisCtrlEvent : TetrisCtrlEventClass = TetrisCtrlEventClass.get()