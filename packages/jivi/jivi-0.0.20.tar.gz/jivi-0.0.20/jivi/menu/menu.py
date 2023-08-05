from __future__ 			import annotations
from typing 				import List
from ..util  				import first_index,first_item,good_list_index,all_true,convert_func,String
from curses.textpad 		import rectangle
from time 					import sleep,time
import curses
import math


class Event:

	class Event:
		debug = False
		__registered_funcs : List[callable]
		def __init__(self,ctrl):
			self.ctrl = ctrl
			self.__registered_funcs = []
		
		@property
		def menu(self):
			return self.ctrl.active_menu
		
		def before_fire(self,*a,**b):
			pass
		def fire(self,*a,**b):
			self.before_fire(*a,**b)
			for f in self.__registered_funcs:

				f(self)
		
		def __call__(self,condition=None):
			def decorator(f):
				if condition is not None:
					def new_func(*a,**b):
						if condition(*a,**b):
							f(*a,**b)
					self.register_func(new_func)
					return new_func
				self.register_func(f)
				return f
			return decorator
		def init(self):
			pass

		def register_func(self,func):
			self.__registered_funcs.append(func)
	
	class MouseClick(Event):
		coord        : Position
		def before_fire(self,*a,**b):
			id, mx, my, z, bstate= curses.getmouse()
			self.coord = Position(mx,my)

	class CharReceived(Event):
		received:InputChar = None
		def before_fire(self,received:InputChar,*a,**b):
			self.received = received

	class FocusedOnListChanged(Event):
		focused_now:bool=False
		def before_fire(self,focused_now,*a,**b):
			self.focused_now = focused_now

class Events:
	mouse_down 				= Event.MouseClick
	mouse_up   				= Event.MouseClick
	mouse_clicked			: Event.MouseClick
	building_print			: Event.Event
	char_received 			: Event.CharReceived
	selected_changed_manual : Event.Event
	print_build 		    : Event.Event
	after_print 		    : Event.Event
	focused_on_list_changed	: Event.FocusedOnListChanged


	def __init__(self,ctrl):
		self.mouse_clicked				= Event.MouseClick(ctrl)
		self.mouse_down 				= Event.MouseClick(ctrl)
		self.mouse_up   				= Event.MouseClick(ctrl)
		self.char_received 				= Event.CharReceived(ctrl)
		self.building_print				= Event.Event(ctrl)
		self.print_build				= Event.Event(ctrl)
		self.after_print				= Event.Event(ctrl)
		self.selected_changed_manual 	= Event.Event(ctrl)
		self.focused_on_list_changed	= Event.FocusedOnListChanged(ctrl)

		@self.mouse_up()
		def d(me:MouseClick):
			print("UP")
			print(me.Position)
			print("\n"*4)
		@self.mouse_down()
		def d(me:MouseClick):
			print("DOWN")
			print(me.Position)
			print("\n"*4)
	def init(self):
		for d in filter(lambda x : isinstance(getattr(self,x),Event), dir(self)):
			getattr(self,d).init()





class MouseState:
	pressed = False
	released = False
	bstate : int
	def __init__(self,bstate:int):
		self.bstate = bstate
		if bstate == 0:
			self.pressed = True
		if bstate == 1:
			self.released = True
		
	def __repr__(self):
		return f"p {self.pressed} r {self.released} s {self.bstate}"
	


#BUTTONn_PRESSED, BUTTONn_RELEASED, BUTTONn_CLICKED, BUTTONn_DOUBLE_CLICKED, BUTTONn_TRIPLE_CLICKED, BUTTON_SHIFT, BUTTON_CTRL, BUTTON_ALT




class LineConstructor:
	def __init__(self,text:str='',selected:bool=False,color:int=None,underline:bool=False,bold:bool=False,prefix:str='',add_line_break:bool=True,empty:int=0,x:int=None,y:int=None):
		self.text           = text
		self.selected       = selected
		self.color          = color
		self.underline      = underline
		self.bold           = bold
		self.prefix         = prefix
		self.add_line_break = add_line_break
		self.empty          = empty
		self.x              = x
		self.y              = y
	@property
	def attr(self):
		color = (33554432 if self.selected else 16777216) if self.color is None else self.color
		val  = color
		for should_do,attrValue in filter(lambda x : x[0],[[self.underline,curses.A_UNDERLINE],[self.bold,curses.A_BOLD]]):
			val = val | attrValue
		return val
	
	@property
	def line_height(self):
		if self.empty:
			return self.empty
		if self.add_line_break:
			return 1
		return 0
	
	def __repr__(self):
		return f'LineConstructor {self.prefix}{self.text}'
class Position:
	def __init__(self,x:int,y:int):
		self.x = x
		self.y = y
	def __repr__(self):
		return f'Position ({self.x},{self.y})'

	@classmethod
	def reversed(cls,y:int,x:int):
		return cls(x,y)
class Area:
	on_click:callable = None
	def pos_is_in(self,pos:Position) -> bool:
		return False
	def handle_click(self,pos:Position,*a,**b):
		if not self.on_click:
			return
		if self.pos_is_in(pos):
			self.on_click(*a,**b)


class LineArea(Area):
	def __init__(self,y:int,start_x:int,stop_x:int):
		self.y       = y
		self.start_x = start_x
		self.stop_x  = stop_x
	def pos_is_in(self,pos:Position) -> bool:
		return (pos.y == self.y) and (self.start_x <= pos.x <= self.stop_x)
	def __repr__(self):
		return f'LineArea [{self.y}][{self.start_x}-{self.stop_x}]'
class LinesArea(Area):
	lines : List[LineArea] = []
	def __init__(self):
		self.lines = []
	def append(self,line:LineArea):
		self.lines.append(line)
	def reset(self):
		self.lines = []
	def pos_is_in(self,pos:Position) -> bool:
		for l in self.lines:
			if l.pos_is_in(pos):
				return True
		return False
	def add_dummy(self,n=1):
		for i in range(n):
			self.append(LineArea(0,0,0))
	@property
	def line_range(self):
		if not self.lines:
			return [None,None]
		ar    = [l.y for l in self.lines]
		return [min(ar),max(ar)]

	def __repr__(self):
		sval = ','.join([str(x) for x in self.lines])
		return f'LinesArea {sval}]'
class InputChar:
	def __init__(self,code:int,name:str=None):
		self.code = code
		self.name = Curses.get_keyname(code) if name is None else name
		self.c    = chr(code)
	def __repr__(self):
		return f'Code : {self.code} c : {self.c} name : {self.name}'

	@classmethod
	def from_ch(cls,code:int=None) -> InputChar:
		return InputChar(code=code) if not (code is None or (code < 0)) else None
	
class Button(LinesArea):
	def __init__(self,text:str, win : curses.window,on_click=None,top=None,left=None,right=None,bottom=None):
		uly = 0
		ulx = 0
		lry = 0
		lrx = 0
		if top is not None:
			uly = top
			lry = uly + 2
		if bottom is not None:
			lry = bottom
			uly = lry - 2
		if left is not None:
			ulx = left
			lrx = ulx + len(text) + 2
		if right is not None:
			lrx = right
			ulx = lrx - len(text) - 2

		self.rec      = rectangle(win,uly,ulx,lry,lrx)
		self.text     = text
		self.on_click = on_click
		for y in range(uly,lry):
			self.append(LineArea(y,ulx,lrx))
		
		win.addstr(uly+1,ulx+1,text,LineConstructor(selected=True,bold=True,underline=True).attr)

class LineBlock(Area):
	lines : List[LineConstructor]
	on_click : callable
	linesDrawn : LinesArea
	item_index : int
	def __init__(self,*lines:List[LineConstructor],on_click:callable=None,on_click_ar=[],on_click_p=dict()):
		self.lines       = lines
		self.on_click    = on_click
		self.on_click_ar = on_click_ar
		self.on_click_p  = on_click_p
		self.linesDrawn  = LinesArea()
		self.item_index  = None

	def append(self,line:LineConstructor):
		self.lines.append(line)
	
	@property
	def line_height(self):
		return sum(l.line_height for l in self.lines)
	
	def pos_is_in(self,pos:Position) -> bool:
		return self.linesDrawn.pos_is_in(pos)
	
	def handle_mouse_clicked(self,pos:Position):
		if not self.on_click:
			return
		if self.pos_is_in(pos):
			self.on_click(*self.on_click_ar,**self.on_click_p)
	@property
	def line_range(self):
		return self.linesDrawn.line_range
	
class Curses:
	class _Color:
		normal   : int
		selected : int
		blue     : int
		mag      : int
		fullcyan : int
		def __init__(self,normal:int=0,selected:int=0):
			curses.start_color()
			def get(index:int,font:int,back:int) -> int:
				curses.init_pair(index,font,back)
				return curses.color_pair(index)
			self.normal		= get(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
			self.selected 	= get(2, curses.COLOR_BLACK, curses.COLOR_CYAN)
			self.blue		= get(3, curses.COLOR_WHITE, curses.COLOR_BLUE)
			self.mag		= get(4, curses.COLOR_WHITE, curses.COLOR_MAGENTA)
			self.fullcyan	= get(4, curses.COLOR_CYAN, curses.COLOR_CYAN)

	color            : _Color             
	win              : curses.window       

	def __init__(self,max_lines:int=30):
		self.init()
		win : curses.window 	= curses.initscr()
		self.max_lines			= max_lines
		self.win 				= win
		self.color 				= Curses._Color()
		curses.mousemask(1)
		win.keypad(1)
		curses.mouseinterval(50)

	def clear(self):
		self.win.erase()
	
	def refresh(self):
		self.win.refresh()

	def stop(self):
		self.clear()
		self.refresh()
		curses.endwin()

	def draw_line_old(self,line:LineConstructor):
		if line.empty:
			self.win.addstr("\n"*line.empty)
			return
	
		color = (self.color.selected if line.selected else self.color.normal) if line.color is None else line.color
		attr  = color
		for should_do,attrValue in filter(lambda x : x[0],[[line.underline,curses.A_UNDERLINE],[line.bold,curses.A_BOLD]]):
			attr = attr | attrValue
		if line.prefix:
			self.win.addstr(line.prefix)
		self.win.addstr(line.text,attr)
		if line.add_line_break:
			self.win.addstr("\n")
	


	def parse_block(self,block:LineBlock):
		self.drawLines(block.lines,block.linesDrawn)
	
	def drawLines(self,lines:List[LineConstructor]=[],linesArea:LinesArea=None,debug=False) -> LinesArea:
		def draw_line(line:LineConstructor):
			color = (self.color.selected if line.selected else self.color.normal) if line.color is None else line.color
			attr  = color
			for should_do,attrValue in filter(lambda x : x[0],[[line.underline,curses.A_UNDERLINE],[line.bold,curses.A_BOLD]]):
				attr = attr | attrValue
			if line.prefix:
				self.win.addstr(line.prefix)
			if line.x is not None and line.y is not None:
				self.win.addstr(line.y,line.x,line.text,attr)
			else:
				self.win.addstr(line.text,attr)
		
	
		retval = LinesArea() if linesArea is None else linesArea
		for l in lines:
			
			if l.empty:
				self.win.addstr("\n"*l.empty)
			else:
				start_pos = self.cursor_position
				draw_line(l)
				
				end_pos = self.cursor_position
				
				retval.append(LineArea(start_pos.y,start_pos.x,end_pos.x))
				if l.add_line_break:
					self.win.addstr("\n")

		return retval

	@property
	def max_x(self):
		return self.win.getmaxyx()[1]
	@property
	def max_y(self):
		return self.win.getmaxyx()[0]
	@property
	def cursor_position(self) -> Position:
		return Position.reversed(*self.win.getyx())
	
	def input(self) -> InputChar:
		return InputChar.from_ch(self.win.getch())



	@classmethod
	def get_mouse(cls):
		_, mx, my, _, _ = curses.getmouse()
		return Position(mx,my)

	@classmethod
	def get_keyname(cls,keyname,quit=False):
		start_val = keyname
		if isinstance(keyname,int):
			if keyname in cls.codeToName:
				return cls.codeToName[keyname]
			keyname = chr(keyname)
		if keyname in cls.nameToCode:
			return keyname
		if len(keyname) == 1:
			code = ord(keyname)
			if code in cls.codeToName:
				return cls.codeToName[code]
		if quit:


			print(f'Invalid keyname {keyname} {start_val}')

			print(cls.codeToName)
			exit()
		return None
	
	__init_done = False


	@classmethod
	def init(cls):
		if cls.__init_done:
			return
		cls.__init_done = True
		cls.codeToName = {int(v) : k.lower()[4:] for k,v in curses.__dict__.items() if k.lower().startswith('key_')}
		extra_keys = dict(
			enter=[10,459],
			esc=[27],
			backspace=[8],
			tab=[9],
			mup=[],
			m1released=[1],
			m2pressed=[2]
		)
		for keyname,codes in extra_keys.items():
			for code in codes:
				cls.codeToName[code] = keyname
		cls.nameToCode = dict()
		for k,v in cls.codeToName.items():
			if not v in cls.nameToCode:
				cls.nameToCode[v] = []
			cls.nameToCode[v].append(k)

def find_index(list:List[MenuItem],index):
	for i in range(len(list)):
		if list[i].index == index:
			return i
	return -1


class MenuItem:
	index       : int       = -1
	menu        : Menu      = None
	text        : str       = ""
	action_func : callable  = None
	data	    : any		= None
	def __init__(self,text:str="text",menu:Menu=None,action_func:callable=None,data=None):
		self.text        = text
		self.menu        = menu
		self.action_func = action_func
		self.data		 = data
		self.menu.register_item(self)
	
	@property
	def is_selected(self):
		return self.menu.selected_item_index == self.index
	
	def action(self):
		if self.action_func:
			self.action_func(self)
	
	@property
	def filter_index(self):
		return find_index(self.menu.f_items,self.index)
	
	@property
	def display_index(self):
		return find_index(self.menu.d_items,self.index)
	
	@property
	def ctrl(self):
		return self.menu.ctrl
	
	def on_click(self):
		self.action()
	
	def write(self,terminalPart:TerminalPart,last_one:bool=False):
		l = len(str(len(self.menu.items)))
		prefix = f'{str(self.display_index).zfill(l)} .'
		prefix = f'{str(self.index).zfill(l)} {str(self.display_index).zfill(l)} .'
		prefix = f'{str(self.index).zfill(l)} {str(self.display_index).zfill(l)} {str(self.filter_index).zfill(l)} .  '
		add_line_break = not last_one
		


		terminalPart.create_block(LineConstructor(text=self.text,selected=self.is_selected,prefix=prefix,add_line_break=add_line_break),on_click=self.on_click)
	
	def __repr__(self):
		return f"[MenuItem] {self.index}"
	
class Menu:
	ctrl                : Ctrl           = None
	menu_index          : int            = -1
	items               : List[MenuItem] = []
	f_items             : List[MenuItem] = []
	d_items             : List[MenuItem] = []
	title               : str            = ""
	selected_item_index : int            = -1
	d_max_len			: int			 = 0
	__d_first_f_index	: int			 = 0
	not_manual		    : bool		 	 = False

	def __init__(self,title="Title",ctrl:Ctrl=None):
		self.title               = title
		self.ctrl                = ctrl
		self.d_max_len           = ctrl.cur.max_lines
		self.f_items             = []
		self.d_items             = []
		self.items               = []
		self.selected_item_index = 0
		self.ctrl.register_menu(self)
	def reset(self):
		self.f_items             = []
		self.d_items             = []
		self.items               = []
		self.selected_item_index = 0
		self.__d_first_f_index   = 0
	def items_sorted_by_text(self,items) -> List[MenuItem]:
		return list(sorted(items, key = lambda x : x.text.lower()))
	
	@property
	def d_first_f_index(self):
		return self.__d_first_f_index
	
	@d_first_f_index.setter
	def d_first_f_index(self,value):
		next_val = min(len(self.f_items) - self.d_max_len,value)
		next_val = max(0,next_val)
		self.__d_first_f_index = next_val
	
	@property
	def f_selected_index(self):
		return find_index(self.f_items,self.selected_item_index)
	
	@f_selected_index.setter
	def f_selected_index(self,f_new_index):
		gli           = good_list_index
		f_len         = len(self.f_items)
		f_last_index  = self.f_selected_index
		f_new_index   = gli(f_new_index,f_len)
		f_delta_index = f_new_index - f_last_index

		if not f_len:
			return
		
		if f_delta_index == 0:
			return
		
		last_sel_was_at_bot = self.d_items and self.d_items[-1] == self.selected_item_index
		last_sel_was_at_top = self.d_items and self.d_items[0]  == self.selected_item_index
		going_one_down 		= f_delta_index == 1
		going_one_up   		= f_delta_index == -1

		if going_one_down and last_sel_was_at_bot:
			self.d_first_f_index += 1
		elif going_one_up and last_sel_was_at_top:
			self.d_first_f_index -= 1
		else:
			self.d_first_f_index = f_new_index - math.floor(self.d_max_len/2)


		self.selected_item_index = self.f_items[f_new_index].index

		if self.not_manual:
			self.not_manual = False
		else:
			self.ctrl.event.selected_changed_manual.fire()

	def set_filter_selected_not_manual(self,index):
		self.not_manual       = True
		self.f_selected_index = index
		self.not_manual       = False
	
	@property
	def d_selected_index(self):
		return find_index(self.d_items,self.selected_item_index)
	
	def register_item(self,item:MenuItem):
		item.index = len(self.items)
		self.items.append(item)
	
	@property
	def selected_item(self):
		try:
			retval = self.items[self.selected_item_index]
			return retval
		except:
			return False
		
	def setActive(self):
		self.ctrl.active_menu_index = self.menu_index
	@property
	def active(self):
		return self.menu_index == self.ctrl.menu_active_index


	def print_info(self):
		print('----------\n')
		ar = []
		for k,v in dict(
			selected_item_index=self.selected_item_index,
			f_selected_index=self.f_selected_index,
			d_first_f_index=self.d_first_f_index,
			f_items_l=len(self.f_items),
			d_items_l=len(self.d_items)).items():
			ar.append([k,str(v)])
		for x in String.same_len_ar(ar):
			print(x)
	
	def set_item_f(self):
		self.f_items	= [item for item in self.items if all_true(self.ctrl.filters,item)]
	def set_item_d(self,max_lines=None):
		if max_lines is not None:
			self.d_max_len = max_lines
		self.d_items	= self.f_items[self.d_first_f_index:self.d_first_f_index+self.d_max_len]
	
	
	def item(self,text:str,data=None):
		def decor(f):
			item = MenuItem(text=text,menu=self,action_func=f,data=data)
			return f
		return decor
	
	def one_up(self):
		self.f_selected_index -= 1

	def one_down(self):
		self.f_selected_index += 1

	def page_up(self):
		self.f_selected_index -= self.d_max_len

	def page_down(self):
		self.f_selected_index += self.d_max_len
	



class TerminalPart:
	blocks : List[LineBlock]
	ctrl   : Ctrl

	def __init__(self,ctrl:Ctrl):
		self.ctrl   = ctrl
		self.blocks = []

		@ctrl.event.mouse_clicked()
		def on_click(ev:Event.MouseClick):
			for b in self.blocks:
				b.handle_mouse_clicked(ev.coord)

	def wrapper(self,*lines:List[LineConstructor],on_click_ar=[],on_click_p=dict()):
		def dec(on_click):
			self.append(LineBlock(*lines,on_click=on_click,on_click_ar=on_click_ar,on_click_p=on_click_p))
			return on_click
		return dec
	
	def create_block(self,*lines:List[LineConstructor],on_click:callable=None,on_click_ar=[],on_click_p=dict()):
		self.append(LineBlock(*lines,on_click=on_click,on_click_ar=on_click_ar,on_click_p=on_click_p))
	
	def append(self,block:LineBlock):
		self.blocks.append(block)

	@property
	def line_height(self):
		return sum(b.line_height for b in self.blocks)

	@property
	def line_range(self):
		ar = []
		for block in self.blocks:
			val = block.line_range
			if val is not None:
				ar += val


		if not ar:
			return [None,None]
		return [min(ar),max(ar)]
	
	def write(self,c:Curses):
		for block in self.blocks:
			c.parse_block(block)

class ItemTerminalPart(TerminalPart):
	def add_item_index(self,block_index_start:int,item_index:int):
		if len(self.blocks) > block_index_start:
			for i in range(block_index_start,len(self.blocks)):
				self.blocks[i].item_index = item_index
	


	def fix_max_height(self,max_height:int):
		def delete_last_item():
			last_item_index = self.blocks[-1].item_index
			start_len = len(self.blocks)
			while self.blocks and self.blocks[-1].item_index == last_item_index:
				self.blocks = self.blocks[:-1]
		

		if max_height < 0:
			print(f"ItemTerminalPart fix_max_height max_height < 0 {max_height} ")
			exit()
		while self.blocks and (self.line_height > max_height):
			delete_last_item()
	

class Ctrl:

	#waiting_for_input : bool 			 = False
	menus             : List[Menu]       = []
	cur               : Curses           = None
	active_menu_index : int              = -1
	__on_key          : dict             = None
	event             : Events	 		 = None
	__focused_on_list : bool             = True
	running           : bool             = True
	terminal_top      : TerminalPart     = None
	terminal_bot      : TerminalPart     = None
	terminal_items    : ItemTerminalPart = None
	filters			  : List[callable]   = []
	def __init__(self,max_lines=30):
		self.filters 		   = []
		self.cur               = Curses(max_lines=max_lines)
		self.menus             = []
		self.__on_key          = dict()
		self.event             = Events(self)
		self.__focused_on_list = True
		self.running		   = False
		self.terminal_top	   = TerminalPart(self)
		self.terminal_bot	   = TerminalPart(self)
		self.terminal_items	   = ItemTerminalPart(self)
		self.__register_event_listerners()
	@property
	def active_menu(self):
		try:
			retval = self.menus[self.active_menu_index]
			return retval
		except:
			return False

	@property
	def selected_item(self):
		try:
			retval = self.active_menu.selected_item
			return retval
		except:
			return False
	
	def create_menu(self,title:str):
		return Menu(title=title,ctrl=self)
	
	def register_menu(self,menu:Menu):
		menu.menu_index = len(self.menus)
		if self.active_menu_index == -1:
			self.active_menu_index = menu.menu_index
		
		self.menus.append(menu)

	
	@property
	def focused_on_list(self):
		return self.__focused_on_list
	
	@focused_on_list.setter
	def focused_on_list(self,value):
		if value != self.focused_on_list:
			self.__focused_on_list = value
			self.event.focused_on_list_changed.fire(value)

	def __register_event_listerners(self):
		key = self.on_key

		def condition_active_menu_exists(*a,**b):
			return True if self.active_menu else False
		
		@key('esc')
		def f(ctrl:Ctrl):
			ctrl.stop()
		
		@key('up',condition=condition_active_menu_exists,no_para=True)
		def f():	self.active_menu.one_up()
		
		@key('down',condition=condition_active_menu_exists,no_para=True)
		def f():	self.active_menu.one_down()
		
		@key('enter',no_error=True)
		def f(ctrl:Ctrl):				ctrl.selected_item.action()
		
		@key('ppage',condition=condition_active_menu_exists)
		def f(ctrl:Ctrl):				ctrl.active_menu.page_up()
		
		@key('npage',condition=condition_active_menu_exists)
		def f(ctrl:Ctrl): 				ctrl.active_menu.page_down()



		@key(curses.BUTTON1_RELEASED)
		def button_up(ctrl:Ctrl):	
			ctrl.event.mouse_up.fire()


		@key(curses.BUTTON1_PRESSED)
		def mouse_down(ctrl:Ctrl):
			print("pressed")
			ctrl.event.mouse_down.fire()

		@key(curses.KEY_MOUSE)
		def mouse_clicked(ctrl:Ctrl):	
			ctrl.event.mouse_clicked.fire()


		@key(curses.KEY_F10,no_para=True)
		def ok():
			self.active_menu_index = -1
			print(f"self.active_menu_index {self.active_menu_index}")
		@self.event.building_print(condition=condition_active_menu_exists)
		def check_title(ev:Event.Event):
			m = self.active_menu
			if not m.title:
				return
			self.terminal_top.create_block(LineConstructor(text=m.title,underline=True),LineConstructor(empty=1))
	
	def on_key(self,key,func=None,condition=None,no_error=False,no_para=False):

		keyname = Curses.get_keyname(key,quit=True)
		if func is not None:
			self.__on_key[keyname] = convert_func(func,no_error=no_error,condition=condition,no_para=no_para)
			return
		
		def decorator(f):
			ret_func = convert_func(f,no_error=no_error,condition=condition,no_para=no_para)
			self.__on_key[keyname] = ret_func
			return ret_func
		return decorator
	
	def do_key(self,code):
		keyname = Curses.get_keyname(code)
		if not keyname:
			return
		if keyname in self.__on_key:
			self.__on_key[keyname](self)
	
	def exit(self):
		self.stop()
		self.cur.stop()
	def stop(self):
		self.running = False
	
	def display(self):
		self.running = True
		def printer(c:Curses,m:Menu):
			for term in [self.terminal_top,self.terminal_items,self.terminal_bot]:
				term.blocks = []
			c.clear()
			self.cur.max_lines = c.win.getmaxyx()[0] - 1
			m.set_item_f()
			self.event.building_print.fire()
			m.set_item_f()
			m.set_item_d(max_lines=self.cur.max_lines - self.terminal_top.line_height - self.terminal_bot.line_height)
			term_item = self.terminal_items

			d_items_len = len(m.d_items)
			d_items_last_index = len(m.d_items) - 1
			for list_index in range(d_items_len):
				item : MenuItem = m.d_items[list_index]
				last_len 		= len(term_item.blocks)
				item.write(term_item,last_one=list_index==d_items_last_index)
				term_item.add_item_index(last_len,item.index)

			term_item.fix_max_height(self.cur.max_lines - self.terminal_top.line_height - self.terminal_bot.line_height)
			self.event.print_build.fire()


			for term in [self.terminal_top,self.terminal_items,self.terminal_bot]:
				term.write(c)
			
			self.event.after_print.fire()
			inputChar = c.input()
			self.event.char_received.fire(inputChar)
			self.do_key(inputChar.code)

		while self.running and self.active_menu:
			printer(self.cur,self.active_menu)
		self.cur.stop()

	def filter(self,f):
		self.filters.append(f)
		return f