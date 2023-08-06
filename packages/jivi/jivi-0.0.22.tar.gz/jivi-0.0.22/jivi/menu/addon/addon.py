from __future__ 			import annotations
import 					   curses, fnmatch, math
from time 			import time,sleep
from ..menu 		import Menu,MenuItem,TerminalPart,Ctrl,LineConstructor,Event,LinesArea,LineArea
from ...util 		import Thread

class Addon:
	def __init__(self,ctrl:Ctrl):
		self.ctrl = ctrl
	
		self.register_listeners()
	
	@property
	def addstr(self) -> curses.window.addstr:
		return self.cur.win.addstr
	
	@property
	def cur(self):
		return self.ctrl.cur
	
	@property
	def on_key(self):
		return self.ctrl.on_key
	
	@property
	def event(self):
		return self.ctrl.event
	
	@property
	def activeMenu(self):
		return self.ctrl.active_menu
	
	@property
	def selectedItem(self):
		return self.ctrl.selected_item
	
	def register_listeners(self):
		pass


class FirstLetter(Addon):
	total_received : str 
	last_done      : int 
	enabled        : bool

	def reset(self):
		self.total_received = ""
		self.last_done      = 0
	def register_listeners(self):
		self.total_received = ""
		self.last_done      = 0
		self.enabled        = True
		event               = self.event
		on_key              = self.on_key
		
		@event.focused_on_list_changed()
		def focused_on_list_changed(ev:Event.FocusedOnListChanged):
			self.reset()
			self.enabled = ev.focused_now

		@event.selected_changed_manual()
		def changed(ev:Event.Event):
			self.reset()
		
		@event.char_received()
		def on_char_received(ev:Event.CharReceived):
			if not self.enabled:
				return
			
			if (time() - self.last_done) > 1:
				self.total_received = ""
			received = ev.received
			if received.name is None and received.c:
				self.total_received += received.c
			else:
				self.total_received = ''
			self.last_done = time()
			menu = self.activeMenu
			if not menu:
				return
			
			if self.total_received:
				for item in menu.items_sorted_by_text(menu.f_items):
					if item.text.lower().startswith(self.total_received):
						return menu.set_filter_selected_not_manual(item.filter_index)

class Mousedownwatcher:
	def __init__(self,scrollbar:Scrollbar):
		self.scrollbar = scrollbar
		self.register_listeners()
		self.last_event = 0
	@property
	def ctrl(self):
		return self.scrollbar.ctrl

	@property
	def addstr(self) -> curses.window.addstr:
		return self.cur.win.addstr
	
	@property
	def cur(self):
		return self.ctrl.cur
	
	@property
	def on_key(self):
		return self.ctrl.on_key
	
	@property
	def event(self):
		return self.ctrl.event
	
	@property
	def activeMenu(self):
		return self.ctrl.active_menu
	
	@property
	def selectedItem(self):
		return self.ctrl.selected_item

	@property
	def area_plus(self):
		return self.scrollbar.area_plus
	
	@property
	def area_min(self):
		return self.scrollbar.area_min

	def mouse_down_thread(self,func,last_event):
		print(f"mouse_down_thread started {func.__name__}")
		func()
		sleep(0.5)
		while last_event == self.last_event:
			func()
			sleep(0.5)
		print(f"mouse_down_thread stop {func.__name__}")

	def register_listeners(self):
		events = self.ctrl.event
		cur    = self.cur

		@events.mouse_down()
		def mc(ev:Event.MouseClick):
			print(f"received mouse_down")
			last_event      = time()
			self.last_event = last_event
			pos             = ev.coord
			m = self.activeMenu
			if not m:
				return
			
			if self.area_plus.pos_is_in(pos):
				Thread(self.mouse_down_thread,(m.page_down,last_event))
			if self.area_min.pos_is_in(pos):
				Thread(self.mouse_down_thread,(m.page_up,last_event))

		@events.mouse_up()
		def mc(ev:Event.MouseClick):
			print(f"received mouse up")
			self.last_event = time()
	

class Scrollbar(Addon):
	area_plus        : LinesArea       
	area_min         : LinesArea       
	mousedownwatcher : Mousedownwatcher
	def print_scrollbar(self,min_y,max_y,x):
		color                 = self.cur.color.selected
		addstr                = self.cur.win.addstr
		self.mousedownwatcher = Mousedownwatcher(self)
		def print_button(start_y,s,area:LinesArea):
			texts = ["   ","   "]
			for i,line in enumerate(area.lines):
				line         : LineArea = line
				line.y                  = start_y+i
				line.start_x            = x-3
				line.stop_x             = x
				addstr(line.y,line.start_x,texts[i],self.cur.color.blue)
		
		print_button(min_y,"-",self.area_min)
		print_button(max_y - 1,"+",self.area_plus)

		def print_scrollbar(start_y,stop_y,start_x):
			m = self.activeMenu
			length 		 = max_y - min_y - 3
			position_now = math.ceil( ((m.f_selected_index + 1)/ len(m.f_items)) * length + min_y + 1)
			for line in range(start_y,stop_y):
				col = self.cur.color.mag
				if position_now == line:
					col = self.cur.color.blue
				addstr(line,start_x," ",col)
		
		print_scrollbar(min_y + 2, max_y - 1, x - 2)
	
	def register_listeners(self):
		def get_dummy_lines_area():
			x = LinesArea()
			for i in range(2):
				x.append(LineArea(0,0,0))
			return x
		self.area_plus = get_dummy_lines_area()
		self.area_min  = get_dummy_lines_area()
		events         = self.ctrl.event
		cur            = self.cur

		@events.mouse_clicked()
		def mc(ev:Event.MouseClick):
			pos = ev.coord

			m = self.activeMenu
			if not m:
				return
			
			if self.area_plus.pos_is_in(pos):
				m.page_down()
			if self.area_min.pos_is_in(pos):
				m.page_up()

		@events.after_print()
		def build_print(ev:Event.Event):
			old_cursor = cur.cursor_position
			min_y,max_y = self.ctrl.terminal_items.line_range
			if min_y is None:
				return
			max_x = cur.max_x
			self.print_scrollbar(min_y,max_y,max_x)
			cur.win.move(old_cursor.y,old_cursor.x)

class Searchbox(Addon):
	area_input  					: LinesArea
	searching                       : bool = False
	first_build_since_input_changed : bool = False
	__search_input                  : str  = ""
	width : int = 20
	height : int = 1

	@property
	def search_input(self):
		return self.__search_input

	@search_input.setter
	def search_input(self,value):
		if value != self.__search_input:
			self.__search_input = value
			if value:
				self.first_build_since_input_changed = True
	

	def on_activate(self):
		self.searching = True
		cur       = self.cur
		last_line = self.area_input.lines[-1]

		cur.win.move(last_line.y,last_line.start_x)
		curses.curs_set(2)
		cur.win.refresh()

	
	def stop_searching(self):
		self.searching = False
	
	def on_searching(self):
		cur       = self.cur
		last_line = self.area_input.lines[-1]

		self.addstr(last_line.y,last_line.start_x,self.search_input,cur.color.selected)
		
		curses.curs_set(2)
		cur.win.refresh()

	
	def print_search_input(self,window_width):
		if len(self.area_input.lines) != self.height:
			self.area_input.lines = self.area_input.lines[:self.height]
			self.area_input.add_dummy(self.height - len(self.area_input.lines))
		
				
		
		addstr = self.addstr
		for i in range(self.height):
			addstr(i,window_width - self.width,"_"*self.width,self.cur.color.fullcyan)
			self.area_input.lines[i].y = i
			self.area_input.lines[i].start_x = window_width - self.width
			self.area_input.lines[i].stop_x = window_width

	def register_listeners(self):
		self.area_input                      = LinesArea()
		self.__search_input                  = ""
		self.searching                       = False
		self.first_build_since_input_changed = False
		events                               = self.ctrl.event
		on_key                               = self.ctrl.on_key
		cur                                  = self.cur

		for i in range(self.height):
			self.area_input.append(LineArea(0,0,0))
			self.area_input.append(LineArea(0,0,0))


		def leave_search():

			self.searching = False

		@self.ctrl.filter
		def filter(mi:MenuItem):
			if not self.searching:
				return True
			if not self.search_input:
				return True
			return fnmatch.fnmatch(mi.text,'*' + self.search_input + '*')

		@on_key(curses.KEY_F2)
		def toggle_searching(ctrl:Ctrl):
			self.search_input 		= ''
			self.searching 			= not self.searching
			ctrl.focused_on_list 	= not self.searching
		
		@on_key(curses.KEY_BACKSPACE)
		def back_space(ctrl:Ctrl):
			if self.searching:
				self.search_input = self.search_input[:-1]
				if not self.search_input:
					self.stop_searching()
		
		@events.char_received()
		def ok(ev:Event.CharReceived):
			inp = ev.received
			if self.searching and (inp.c) and (not inp.name):
				self.search_input = self.search_input + inp.c
			
		@events.after_print()
		def build_print(ev:Event.Event):
			old_cursor = cur.cursor_position
			self.print_search_input(cur.max_x)
			cur.win.move(old_cursor.y,old_cursor.x)
			if self.searching:
				self.on_searching()

		@events.mouse_clicked()
		def searchbox_mc(ev:Event.MouseClick):
			pos = ev.coord
			m = self.activeMenu
			if not m:
				return
			
			if self.area_input.pos_is_in(pos):
				self.on_activate()
		
		@events.building_print()
		def build_print(ev:Event.Event):
			first_build = self.first_build_since_input_changed
			self.first_build_since_input_changed = False
			if not self.searching:
				return
			
			menu = self.activeMenu
			if not menu:
				return
			
			bottom = self.ctrl.terminal_bot
			bottom.create_block(LineConstructor(empty=2))
			@bottom.wrapper(LineConstructor(text=f'#results : {len(menu.f_items)}/{len(menu.items)}'),LineConstructor(text=f'Searching : {self.search_input}',add_line_break=False))
			def kk(*a,**b):
				print(f"a {a}")
				print(f"b {b}")
			
			if first_build:
				menu.d_first_f_index = 0

class Searcher(Addon):
	searching : bool = False

	first_build_since_input_changed : bool = False
	__search_input : str = ""

	@property
	def search_input(self):
		return self.__search_input

	@search_input.setter
	def search_input(self,value):
		if value != self.__search_input:
			self.__search_input = value
			if value:
				self.first_build_since_input_changed = True
	
	def register_listeners(self):
		self.__search_input = ""
		self.searching = False
		self.first_build_since_input_changed = False

		events = self.ctrl.event
		on_key = self.ctrl.on_key
		
		@self.ctrl.filter
		def filter(mi:MenuItem):
			if not self.searching:
				return True
			if not self.search_input:
				return True
			return fnmatch.fnmatch(mi.text,'*' + self.search_input + '*')
		
		@on_key(curses.KEY_F2)
		def toggle_searching(ctrl:Ctrl):
			self.search_input 		= ''
			self.searching 			= not self.searching
			ctrl.focused_on_list 	= not self.searching
		
		@on_key(curses.KEY_BACKSPACE)
		def back_space(ctrl:Ctrl):
			if self.searching:
				self.search_input = self.search_input[:-1]
		
		@events.char_received()
		def ok(ev:Event.CharReceived):
			inp = ev.received
			if self.searching and (inp.c) and (not inp.name):
				self.search_input = self.search_input + inp.c
			
		@events.building_print()
		def build_print(ev:Event.Event):
			first_build = self.first_build_since_input_changed
			self.first_build_since_input_changed = False
			if not self.searching:
				return
			
			menu = self.activeMenu
			if not menu:
				return
			
			bottom = self.ctrl.terminal_bot

			bottom.create_block(LineConstructor(empty=2))
			@bottom.wrapper(LineConstructor(text=f'#results : {len(menu.f_items)}/{len(menu.items)}'),LineConstructor(text=f'Searching : {self.search_input}',add_line_break=False))
			def kk(*a,**b):
				print(f"a {a}")
				print(f"b {b}")
			
			if first_build:
				menu.d_first_f_index = 0

class Searcher(Addon):
	searching : bool = False

	first_build_since_input_changed : bool = False
	__search_input : str = ""

	@property
	def search_input(self):
		return self.__search_input

	@search_input.setter
	def search_input(self,value):
		if value != self.__search_input:
			self.__search_input = value
			if value:
				self.first_build_since_input_changed = True
	
	def register_listeners(self):
		self.__search_input = ""
		self.searching = False
		self.first_build_since_input_changed = False

		events = self.ctrl.event
		on_key = self.ctrl.on_key
		
		@self.ctrl.filter
		def filter(mi:MenuItem):
			if not self.searching:
				return True
			if not self.search_input:
				return True
			return fnmatch.fnmatch(mi.text,'*' + self.search_input + '*')
		
		@on_key(curses.KEY_F2)
		def toggle_searching(ctrl:Ctrl):
			self.search_input 		= ''
			self.searching 			= not self.searching
			ctrl.focused_on_list 	= not self.searching
		
		@on_key(curses.KEY_BACKSPACE)
		def back_space(ctrl:Ctrl):
			if self.searching:
				self.search_input = self.search_input[:-1]
		
		@events.char_received()
		def ok(ev:Event.CharReceived):
			inp = ev.received
			if self.searching and (inp.c) and (not inp.name):
				self.search_input = self.search_input + inp.c
			
		@events.building_print()
		def build_print(ev:Event.Event):
			first_build = self.first_build_since_input_changed
			self.first_build_since_input_changed = False
			if not self.searching:
				return
			
			menu = self.activeMenu
			if not menu:
				return
			
			bottom = self.ctrl.terminal_bot

			bottom.create_block(LineConstructor(empty=2))
			@bottom.wrapper(LineConstructor(text=f'#results : {len(menu.f_items)}/{len(menu.items)}'),LineConstructor(text=f'Searching : {self.search_input}',add_line_break=False))
			def kk(*a,**b):
				print(f"a {a}")
				print(f"b {b}")
			
			if first_build:
				menu.d_first_f_index = 0