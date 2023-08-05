from __future__ import annotations
from jivi import jvWrapper
import fnmatch,curses, math
from time import time
from typing import List,Dict

@jvWrapper()
class CoordinateStartStop:
	def __init__(self,start:int,stop:int):
		self.start = start
		self.stop  = stop
		self.delta = stop - start

@jvWrapper()
class Coordinate:
	def __init__(self,x:int,y:int):
		self.x = x
		self.y = y

@jvWrapper()
class MouseClick:
	def __init__(self,x:int,y:int):
		self.x = x
		self.y = y
		self.t = time()

class LineResponse:
	def __init__(self,start:Coordinate,stop:Coordinate):
		self.start = start
		self.stop  = stop
	def __repr__(self):
		return f'{self.start} -> {self.stop}'

@jvWrapper()
class InputChar:
	code:int
	c:str
	name:str
	def __init__(self,code:int,name:str=None):
		self.code = code
		self.c = chr(code)
		self.name = name
	
	def __repr__(self):
		return f'Code : {self.code} c : {self.c} name : {self.name}'

@jvWrapper(propnames_to_skip=['item'])
class MenuItemToDisplay:
	x_data : CoordinateStartStop
	line_number = -1
	def __init__(self,row_number:int,result_number:int,selected:bool,item:MenuItem):
		self.row_number = row_number
		self.result_number = result_number
		self.selected = selected
		self.item = item
		self.reset()

	def is_clicked(self,mouse_click:Coordinate):
		if self.line_number != mouse_click.y:
			return False
		#zou nog moeten verbeterd worden....
		return True

	def reset(self):
		self.line_number = -1
		self.x_data : CoordinateStartStop = CoordinateStartStop(-1,-1)
	
	def writeLine(self,C:Curses):
		self.reset()
		ret_val = C.line(self.item.name,selected=self.selected,prefix=f'{str(self.result_number).zfill(2)} {str(self.row_number).zfill(2)}   ')
	
		if ret_val:
			self.line_number = ret_val.start.y
			self.x_data = CoordinateStartStop(ret_val.start.x,ret_val.stop.x)
		return True

@jvWrapper(propnames_to_skip=['func'])
class MenuItem:
	def __init__(self,name,func=None,desc=None,cmd_keys=[],exit_after:bool=False,data=None):
		self.name 			:str		= name
		self.func 						= func
		self.desc 			:str		= desc if desc is not None else name
		self.cmd_keys	  	:List[str]  = cmd_keys
		self.exit_after 				= exit_after
		self.data						= data
	def exec(self,p):
		if not self.func:
			print(f'{self}.exec func is none')
			return
		p.itemClicked = self
		retval = self.func(p)
		# misschien fout hier ?!
		p.itemClicked = None
		if self.exit_after:
			exit()
		return retval

class _SearchFilterHelper:
	@classmethod
	def fnmatch(cls):
		def ret_val(str_to_check:str,looking_for:str):
			return fnmatch.fnmatch(str_to_check,looking_for)
		return ret_val
	@classmethod
	def default(cls):
		def ret_val(str_to_check:str,looking_for:str):
			return fnmatch.fnmatch(str_to_check,'*' + looking_for + '*')
		return ret_val

class SearchFilter:
	fnmatch = _SearchFilterHelper.fnmatch()
	default = _SearchFilterHelper.default()

def _getcurses_codes():
	codeToName = {int(v) : k.lower()[4:] for k,v in curses.__dict__.items() if k.lower().startswith('key_')}
	extra_keys = dict(
		enter=[10,459],
		esc=[27],
		backspace=[8],
		tab=[9]
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
codeToName, nameToCode = _getcurses_codes()

class Curses:
	def __init__(self,stdscr):
		self.stdscr : curses.window = stdscr
		curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
		curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)
		self.colors_normal = curses.color_pair(1)
		self.colors_selected = curses.color_pair(2)
	
	@classmethod
	def keyname(cls,keyname,quit=False):
		if isinstance(keyname,int):
			if keyname in codeToName:
				return codeToName[keyname]
			keyname = chr(keyname)
		if keyname in nameToCode:
			return keyname
		if len(keyname) == 1:
			code = ord(keyname)
			if code in codeToName:
				return codeToName[code]
		if quit:
			print(f'Invalid keyname {keyname}')
			exit()
		return None
	
	def clear(self):
		self.stdscr.erase()
	
	@property
	def cursor_position(self) ->Coordinate:
		y,x = self.stdscr.getyx()
		return Coordinate(x,y)
	
	def emptyLine(self,n=1) ->LineResponse:
		start = self.cursor_position
		self.stdscr.addstr("\n"*n)
		return LineResponse(start,self.cursor_position)
	
	def line(self,txt:str='',selected=False,color=None,underline=False,bold=False,prefix='',add_line_break=True) ->LineResponse:
		start = self.cursor_position
		color = (self.colors_selected if selected else self.colors_normal) if color is None else color
		attr = color
		for should_do,attrValue in [
			[underline,curses.A_UNDERLINE],
			[bold,curses.A_BOLD]]:
			if should_do:
				attr = attr | attrValue
		if prefix:
			self.stdscr.addstr(prefix)
		self.stdscr.addstr(txt,attr)
		stop = self.cursor_position
		if add_line_break:
			self.stdscr.addstr("\n")
		return LineResponse(start,stop)
	
	def get_char(self) -> InputChar:
		code = self.stdscr.getch()
		return InputChar(code=code,name=self.keyname(code))

@jvWrapper(propnames_to_skip=['menu','c','items','itemClicked'])
class Param:
	inputChar   : InputChar         
	menu        : Menu              
	c           : Curses            
	items       : MenuItemCollection
	itemClicked : MenuItem          
	def __init__(self,menu:Menu,title:str,max_rows:int,max_rows_auto:bool,max_amount_rows_not_data:int):
		self.menu                                          = menu
		self.title                                         = title
		self.max_rows                                      = max_rows
		self.max_rows_auto                                 = max_rows_auto
		self.max_amount_rows_not_data                      = max_amount_rows_not_data
		self.items                    : MenuItemCollection = None
		self.itemClicked              : MenuItem           = None
		self.mouseClick               : Coordinate         = None
	
class MenuItemCollectionIndexHelper:
	def __init__(self,p:Param):
		self.p = p
		self.__selected = 0
	
	@property
	def filtered(self):				return self.p.items.filtered

	@property
	def first(self):				return max(0,self.first_item)

	@property
	def last(self):					return min(len(self.filtered) - 1, self.first + self.p.max_rows - 1)

	@property
	def selected(self):				return self.__selected

	@selected.setter
	def selected(self,new_value):
		last_value           = self.__selected
		new_value            = min(max(0,new_value),len(self.filtered)-1)
		delta_selected_index = (new_value-last_value)

		if delta_selected_index == 0:
			return
		elif delta_selected_index == 1:
			#one down
			if (self.last == last_value):
				self.first_item += 1
		elif delta_selected_index == -1:
			#one up
			if (self.first == last_value):
				self.first_item -= 1
		else:
			self.first_item = min(max(0,new_value - math.floor(self.p.max_rows/2)),max(0,len(self.filtered) - self.p.max_rows))
		self.__selected = new_value
	
	def clear(self):
		self.__selected = 0
		self.first_item = 0


@jvWrapper(propnames_to_skip=['p'])
class MenuItemCollection(list):
	to_display : List[MenuItemToDisplay]
	def __init__(self,p:Param, *items:List[MenuItem]):
		self.filtered : List[MenuItem] = []
		self.p = p
		self.p.items = self
		self.filters = []
		self.index = MenuItemCollectionIndexHelper(p)
		self.clear()
		self.append(*items)


		@self.menu.event.mouse_clicked()
		def mouse_clicked(p:Param):
			mouse_click = p.mouseClick
			def get_menuItem_clicked():
				for a in self.to_display:
					if a.is_clicked(mouse_click):
						return a
			menuItemClicked = get_menuItem_clicked()
			if not menuItemClicked:
				return True
			self.index.selected = menuItemClicked.result_number
			self.menu.key.do('enter')
			return True
	
	@jvWrapper()
	def clear(self):
		self.to_display = []
		self.index.clear()
		self.cmd_keys = dict()
		super().clear()
	
	def __check_item(self,item:MenuItem):
		for sc in item.cmd_keys:
			if sc in self.cmd_keys:
				print(f'{sc} {item} already in cmd_keys !')
				continue
			self.cmd_keys[sc] = item
		return True
	
	def append(self,*ar:List[MenuItem]):
		for v in filter(self.__check_item,ar):
			super().append(v)

	
	def __setitem__(self, key, v:MenuItem):
		return super().__setitem__(key, v) if self.__check_item(v) else None
	
	def set_filtered(self) ->List[MenuItem]:
		def check_all_filters(item:MenuItem):
			for filter_function in self.filters:
				if not filter_function(self.p,item):
					return False
			return True
		self.filtered  = list(filter(check_all_filters,self))
		self.p.menu.event_call.items_to_print_loaded()
		return self.filtered
	
	@property
	def selected(self) -> MenuItem:
		try:
			x = self.filtered[self.index.selected]
			return x
		except:
			print(f'Failed so select menuitem len filtered {len(self.filtered)} index : {self.index.selected}')
			return None
		
	def get_to_display(self) -> List[MenuItemToDisplay]:
		self.set_filtered()
		def get_ret_val():
			row_number = 0
			for result_number in range(self.index.first,self.index.last+1):
				row_number += 1
				selected = result_number == self.index.selected
				item = self.filtered[result_number]
				yield MenuItemToDisplay(row_number=row_number,result_number=result_number,selected=selected,item=item)
		self.to_display = list(get_ret_val())
		return self.to_display
	
	@property
	def menu(self) -> Menu:
		return self.p.menu


@jvWrapper(propnames_to_skip=['p'])
class KeyboardEvent:
	def __init__(self,p:Param):
		self.p = p
		self.__tab = dict()
	def __call__(self, keyname):
		keyname = Curses.keyname(keyname,quit=True)
		def decorator(f):
			self.__tab[keyname] = f
			return f
		return decorator
	def do(self,keyname):
		keyname = Curses.keyname(keyname)
		if not keyname:
			return
		if keyname in self.__tab:
			self.__tab[keyname](self.p)

def EventHelper_inner_function():
	def main_decorator(mainf):
		name = mainf.__name__
		def ret_val(self,*a,**b):
			def add_function(func_to_add):
				if not name in self._funcs:
					self._funcs[name] = []
				self._funcs[name].append(func_to_add)
			
			def special_modus():
				if self._modus == 'add':
					add_function(a[0])
					return
				if self._modus == 'call':
					if not name in self._funcs:
						return True
					for func in self._funcs[name]:
						if not func(self.p):
							return False
					return True
					

			if self._modus != 'normal':
				ret_val = special_modus()
				self._modus = 'normal'
				return ret_val
				
			def decorator(f):
				add_function(f)
				return f
			
			return decorator
		return ret_val
	return main_decorator


def EventHelper_inner_function_strontboel():
	def main_decorator(mainf):
		name = mainf.__name__
		def ret_val(self,*a,**b):
			def add_function(func_to_add):
				if not name in self._funcs:	
					self._funcs[name] = []
				self._funcs[name].append(func_to_add)
				return func_to_add

			def decorator(f):
				return add_function(f)
			
			if self._modus == 'normal':		
				return decorator

			if self._modus == 'add':		
				return add_function(a[0])
			
			if self._modus == 'call':
				for func in getattr(self._funcs,name,[]):
					if not func(self.p):
						return False
				return True
			return None
		return ret_val
	return main_decorator

@jvWrapper(propnames_to_skip=['p'])
class MenuEvent:
	_modus  = 'normal'
	__event = EventHelper_inner_function
	def __init__(self,p:Param):
		self._modus = 'normal'
		self.p = p
		self._funcs = dict()
	
	@__event()
	def mouse_clicked(self):			pass
	@__event()
	def curses_started(self):			pass
	@__event()
	def items_to_print_loaded(self):	pass
	@__event()
	def before_menu_build(self):		pass
	@__event()
	def after_menu_build(self):			pass
	@__event()
	def char_received(self):			pass
	@__event()
	def after_items_print(self):		pass

	def _set_modus(self,modus):
		self._modus = modus
		return self
	
	@property
	def add(self):
		return self._set_modus('add')
	
	@property
	def call(self):
		return self._set_modus('call')
	
	@property
	def info(self):
		return self._set_modus('info')


@jvWrapper(propnames_to_skip=['p'])
class MenuStartStringSelect:
	def __init__(self,p:Param):
		self.p = p
		self.enabled = False
		self.input = ''
		self.time_last_added = 0
		self._load_key_listeners()
	
	@property
	def menu(self) -> Menu:
		return self.p.menu
	
	def _load_key_listeners(self):
		key = self.menu.key
		events = self.menu.event
		@events.items_to_print_loaded()
		def items_to_print_loaded(p:Param):
			p.items.filtered.sort(key = lambda x : x.name.lower())
			if not self.enabled:
				return True
			if not self.input:
				return True
			def select_index():
				for i,c in enumerate(p.items.filtered):
					if c.name.lower().startswith(self.input):
						p.items.index.selected = i
						return
			select_index()
			return True
		@events.char_received()
		def input_checker(p:Param):
			inp = p.inputChar
			def valid():
				if p.menu.search.searching:
					print('searching')
					return True
				if inp.name:
					return True
				if not inp.c:
					return True
			if valid():
				self.disable()
				return True
			self.add_char(inp.c)
			return True
	
	def disable(self):
		self.enabled = False
		self.input = ''
		self.time_last_added = 0
	
	def add_char(self,c:str):
		self.enabled = True
		time_now = time()
		if (time_now - self.time_last_added) > 1:
			self.input = ''
		self.time_last_added = time_now
		self.input = self.input + c
		self.input = self.input.lower()
		print(f'input : {self.input}')

@jvWrapper(propnames_to_skip=['p'])
class MouseListener:
	def __init__(self,p:Param):
		self._funcs = dict()
		self.p = p
		self._load_key_listeners()
		
	@property
	def menu(self) -> Menu:
		return self.p.menu
	
	@property
	def mouse_coords(self) -> Coordinate:
		_, mx, my, _, _ = curses.getmouse()
		return Coordinate(mx,my)
	
	def _load_key_listeners(self):
		key = self.menu.key
		events = self.menu.event
		@events.curses_started()
		def curses_started(p:Param):
			curses.mousemask(1)			
			return True
		@key(curses.KEY_MOUSE)
		def on_mouse_click(p:Param):
			p.mouseClick = self.mouse_coords
			p.menu.event_call.mouse_clicked()
			return True
	
@jvWrapper(propnames_to_skip=['p'])
class MenuSearch:
	def __init__(self,p:Param):
		self.p = p
		self.searching = False
		self.search_input = ''
		self._load_key_listeners()
	
	@property
	def menu(self) -> Menu:
		return self.p.menu
	
	def _load_key_listeners(self):
		key = self.menu.key

		@key(curses.KEY_BACKSPACE)
		def back_space(p:Param):
			if self.searching:
				self.search_input = self.search_input[:-1]
			return True
		
		@key('f2')
		def search(p:Param):
			self.searching = not self.searching
			print(f'Searching : {self.searching}')
			self.search_input = ''
		event : MenuEvent = self.p.menu.event

		@event.after_items_print()
		def after_items_print(p:Param):
			print('after_items_print_listener')
			if not self.searching:
				return True
			C = p.c
			C.emptyLine(2)
			C.line(f'#results : {len(self.p.items.filtered)}/{len(self.p.items)}')
			C.line(f'Searching : {self.search_input}',add_line_break=False)
			return True
		
		@event.char_received()
		def char_received(p:Param):
			inp = p.inputChar
			if self.searching and (inp.c) and (not inp.name):
				self.search_input = self.search_input + inp.c
			return True

		
		def search_filter(p:Param,item:MenuItem):
			if not (self.searching and self.search_input):
				return True
			return SearchFilter.default(item.name,self.search_input)
		self.menu.items.filters.append(search_filter)

class Menu:
	def __init__(self,*menuItems : List[MenuItem],start=False,title='',max_rows=25,max_rows_auto=False,max_amount_rows_not_data=7):
		self.p                 = Param(self,title=title,max_rows=max_rows,max_rows_auto=max_rows_auto,max_amount_rows_not_data=7)
		self.key               = KeyboardEvent(self.p)
		self.event             = MenuEvent(self.p)
		self.items             = MenuItemCollection(self.p,*menuItems)
		self.search            = MenuSearch(self.p)
		self.startStringSelect = MenuStartStringSelect(self.p)
		self.mouseListener     = MouseListener(self.p)
		self._load_key_listeners()
	
	def _load_key_listeners(self):
		key = self.key
		@key('esc')
		def f(p:Param):		exit()
		@key('up')
		def f(p:Param):		p.items.index.selected -= 1
		@key('down')
		def f(p:Param):		p.items.index.selected += 1
		@key('enter')
		def f(p:Param):		p.items.selected.exec(p)
		@key('ppage')
		def f(p:Param):		p.items.index.selected -= p.max_rows
		@key('npage')
		def f(p:Param):		p.items.index.selected += p.max_rows
	
		@self.event.curses_started()
		def curses_started(p:Param):
			p.max_rows = curses.LINES - p.max_amount_rows_not_data if p.max_rows_auto else p.max_rows
			return True
	
	@property
	def event_add(self):		return self.event.add

	@property
	def event_call(self):		return self.event.call
	
	def item(self,name,desc=None,cmd_keys=[],exit_after=False,data=None):
		def decorator(f):
			self.items.append(MenuItem(name,f,desc=desc,cmd_keys=cmd_keys,exit_after=exit_after,data=data))
			return f
		return decorator
	
	def display(self):
		def curses_wrapper(stdscr):

			C = Curses(stdscr)
			self.p.c = C
			self.event_call.curses_started()
			def printer():
				if not self.event_call.before_menu_build():
					print(f'before_menu_build failed')
					return False
				
				C.clear()
				if self.p.title:
					C.line(self.p.title,underline=True)
					C.emptyLine(2)
				


				for displayItem in self.items.get_to_display():
					
					displayItem.writeLine(C)
				
				if not self.event_call.after_items_print():
					print(f'after_items_print failed')
					return False
				
				inputChar = C.get_char()
				self.p.inputChar = inputChar
				if not self.event_call.char_received():
					print(f'char_received failed')
					return False
				
				self.key.do(inputChar.code)
				if not self.event_call.after_menu_build():
					print(f'after_menu_build failed')
					return False
			
			while True:
				if printer() == False:
					exit()


		curses.wrapper(curses_wrapper)