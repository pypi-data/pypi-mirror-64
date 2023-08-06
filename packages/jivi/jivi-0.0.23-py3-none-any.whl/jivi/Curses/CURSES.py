from __future__ 			import annotations
import curses
from ..util import random_el,convert_func

class COLOR:
	class B:
		BLACK   = 0
		BLUE    = 0
		CYAN    = 0
		GREEN   = 0
		MAGENTA = 0
		RED     = 0
		WHITE   = 0
		YELLOW  = 0
		ALL     = []
		@classmethod
		def init(cls):
			bad_keys = ["init","ALL","random"]
			for a  in dir(cls):
				if a.startswith('_') or a in bad_keys:
					continue
				val = getattr(curses,f"COLOR_{a}")
				retval = CURSES.create_color(curses.COLOR_BLACK,val)
			
				setattr(cls,a,retval)
				if a != "BLACK":
					cls.ALL.append(retval)
		@classmethod
		def random(cls):
			return random_el(cls.ALL)

	class F:
		BLACK   = 0
		BLUE    = 0
		CYAN    = 0
		GREEN   = 0
		MAGENTA = 0
		RED     = 0
		WHITE   = 0
		YELLOW  = 0
		ALL     = []
		@classmethod
		def init(cls):
			bad_keys = ["init","ALL","random"]
			for a  in dir(cls):
				if a.startswith('_') or a in bad_keys:
					continue
				retval = CURSES.create_color(getattr(curses,f"COLOR_{a}"),curses.COLOR_BLACK)
				setattr(cls,a,retval)
				if a != "BLACK":
					cls.ALL.append(retval)
		
		@classmethod
		def random(cls):
			return random_el(cls.ALL)

	@classmethod
	def init(cls):
		cls.B.init()
		cls.F.init()
		

def _curses_get_keys():
	codeToName = {int(v) : k.lower()[4:] for k,v in curses.__dict__.items() if k.lower().startswith('key_')}
	extra_keys = dict(
		enter=[10,459],
		esc=[27],
		space=[32],
		backspace=[8],
		tab=[9],
		mup=[],
		m1released=[1],
		m2pressed=[2]
	)
	for keyname,codes in extra_keys.items():
		for code in codes:
			codeToName[code] = keyname
	nameToCode = dict()
	for k,v in codeToName.items():
		if not v in nameToCode:
			nameToCode[v] = []
		nameToCode[v].append(k)
	return codeToName,nameToCode

class CURSES:
	codeToName,nameToCode = _curses_get_keys()

	@classmethod
	def get_keyname(cls,keyname,quit=False):
		def failed():
			if quit:


				print(f'Invalid keyname {keyname} {start_val}')

				print(cls.codeToName)
				exit()
			return None

		start_val = keyname
		if isinstance(keyname,int):
			if keyname in cls.codeToName:
				return cls.codeToName[keyname]
			keyname = chr(keyname)
		if keyname in cls.nameToCode:
			return keyname
		if not keyname:
			return failed()
		if len(keyname) == 1:
			code = ord(keyname)
			if code in cls.codeToName:
				return cls.codeToName[code]

		return failed()

	__last_color_index = 1
	@classmethod
	def create_color(cls,font:int,back:int) -> int:
		curses.init_pair(cls.__last_color_index,font,back)
		retval =  curses.color_pair(cls.__last_color_index)
		cls.__last_color_index += 1
		return retval

	@classmethod
	def init(cls):
		COLOR.B.init()
		COLOR.F.init()
	
class Position:
	def __init__(self,x:int,y:int):
		self.x = x
		self.y = y
	def __repr__(self):
		return f'Position ({self.x},{self.y})'

	
	@classmethod
	def reversed(cls,y:int,x:int):
		return cls(x,y)

class InputChar:
	def __init__(self,code:int,name:str=None):
		self.code = code
		self.name = CURSES.get_keyname(code) if name is None else name
		self.c    = chr(code)
	def __repr__(self):
		return f'Code : {self.code} c : {self.c} name : {self.name}'

	@classmethod
	def from_ch(cls,code:int=None) -> InputChar:
		return InputChar(code=code) if not (code is None or (code < 0)) else None

class OnKeyCb:
	def __init__(self,func:callable,args=[],kwargs=dict(),condition=None,no_error=False):
		self.func      = func
		self.condition = condition
		self.no_error  = no_error
		self.args         = args
		self.kwargs         = kwargs


	def do_func(self):
		if self.condition and not self.condition(*self.args,**self.kwargs):
			return
		
		return self.func(*self.args,**self.kwargs)

	
	def call(self):
		if self.no_error:
			try:
				retval = self.do_func()
				return retval
			except:
				pass
		else:
			return self.do_func()



class CursesWrapper:
	win:curses.window
	running:bool=False
	def __init__(self):
		self.__on_key = dict()
		

	def initscr(self,win:curses.window):
		self.win = win
		CURSES.init()

	def on_key_old(self,key,func=None,condition=None,no_error=False,no_para=False,no_main=False):

		# convert_func_options = dict(
		# 	no_error=no_error,
		# 	condition=condition,
		# 	no_para=no_para,
		# 	kwargs=kwargs,
		# 	args=([self] if not no_main else []) + args)

		convert_func_options = dict(
			no_error=no_error,
			condition=condition,
			no_para=no_para)

		keyname = CURSES.get_keyname(key,quit=True)
		if func is not None:
			self.__on_key[keyname] = convert_func(func,**convert_func_options)
			return
		
		def decorator(f):
			ret_func = convert_func(f,**convert_func_options)
			self.__on_key[keyname] = ret_func
			return ret_func
		return decorator

	def on_key(self,key,func=None,condition=None,no_error=False,no_arg_default=False,args=[],kwargs=dict()):
		keyname = CURSES.get_keyname(key,quit=True)
		construct_dict = dict(
			condition=condition,
			no_error=no_error,
			args=args if no_arg_default else [self] + args,
			kwargs=kwargs)
		if func is not None:
			self.__on_key[keyname] = OnKeyCb(func,**construct_dict)
			return
		
		def decorator(f):
			self.__on_key[keyname] = OnKeyCb(f,**construct_dict)
			return f
		return decorator

	def do_key_old(self,code):

		keyname = CURSES.get_keyname(code)
		
		if not keyname:
			return
		if keyname in self.__on_key:
			self.__on_key[keyname](self)
	
	def do_key(self,code):

		keyname = CURSES.get_keyname(code)
		
		if not keyname:
			return
		if keyname in self.__on_key:
			self.__on_key[keyname].call()

	

	def clear(self):
		self.win.erase()
	
	def refresh(self):
		self.win.refresh()

	def stop(self):
		self.clear()
		self.refresh()
		curses.endwin()
		self.running = False

	def key_reader(self):
		self.running = True
		while self.running:
			inputChar = self.input()
			self.do_key(inputChar.code)
	
	def input(self) -> InputChar:
		return InputChar.from_ch(self.win.getch())



def valid_key(inp):
	return True if CURSES.get_keyname(inp) else False


def get_keyname(inp):
	return CURSES.get_keyname(inp)