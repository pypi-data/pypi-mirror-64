from __future__ import annotations
from typing import List,Dict
import curses
import math

class KeyboardInput:
	code:int
	c:str
	name:str

	def __init__(self,code:int):
		self.code = code
		self.c = chr(code)
		self.name = codeToName.get(code,None)

	def __repr__(self):
		return f'Code : {self.code} c : {self.c} name : {self.name}'
class Curses:
	def __init__(self,stdscr):
		self.stdscr : curses.window = stdscr
		curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
		curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)

		self.colors_normal = curses.color_pair(1)
		self.colors_selected = curses.color_pair(2)

	def clear(self):
		self.stdscr.erase()
	
	def emptyLine(self,n=1):
		self.stdscr.addstr("\n"*n)
	
	def line(self,txt:str='',selected=False,color=None,underline=False,bold=False,prefix='',add_line_break=True):
		if color is None:
			color = self.colors_selected if selected else self.colors_normal
		attr = color

		for should_do,attrValue in [
			[underline,curses.A_UNDERLINE],
			[bold,curses.A_BOLD]]:
			if should_do:
				attr = attr | attrValue
				

		
		if prefix:
			self.stdscr.addstr(prefix)
		
		self.stdscr.addstr(txt,attr)
		if add_line_break:
			self.stdscr.addstr("\n")


	def wait_for_input(self):
		code = self.stdscr.getch()
		return KeyboardInput(code)
	

def to_list(x=None,default=None):
	if x is None:
		return default
	
	return x if isinstance(x,list) else [x]


def _getcurses_codes():

	extra_keys = dict(
		enter=[10,459],
		esc=[27],
		backspace=[8]
	)


	codeToName = {}
	for k,v in curses.__dict__.items():
		if not k.lower().startswith('key_'):
			continue
		codeToName[int(v)] = k.lower()[4:]


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





class Command:
	def __init__(self,name,func=None,desc=None,cmd_keys=None,exit_after:bool=False,with_parameters=False):
		self.name 			:str		= name
		self.with_parameters = with_parameters
		self.func 						= func
		self.desc 			:str		= desc if desc is not None else name
		self.cmd_keys	  	:List[str]  = to_list(cmd_keys,[])
		self.exit_after 				= exit_after

	def exec(self,*a):
		if not self.func:
			print(f'{self}.exec func is none')
			return
		if self.with_parameters:
			self.func(*a)
		else:
			self.func()

		if self.exit_after:
			exit()

	def __repr__(self):
		return f'Command : {self.name}'

	
class ItemToPrint:
	def __init__(self,row_number:int,result_number:int,selected:bool,cmd:Command):
		self.row_number = row_number
		self.result_number = result_number
		self.selected = selected
		self.cmd = cmd


class Commands(list):
	def __init__(self, *commands:List[Command],max_rows:int=20):

		self.__selected_index = 0
		self.item_start_index = 0
		self.max_rows = max_rows
		self.commandline_keys = dict()
		self.append(*commands)
		self.search_input = ''
		self._searching = False




	def load_key_listeners(self,menu:Menu):
		@menu.key(curses.KEY_BACKSPACE)
		def back_space(m:Menu):
			print(m.cmds.searching)
			if not m.cmds.searching:
				return
			m.cmds.search_input = m.cmds.search_input[:-1]
	@property
	def searching(self):
		return self._searching

	@searching.setter
	def searching(self,searching):
		if searching == self.searching:
			return
		
		print(f'Set searching : {searching}')
		self._searching = searching

		self.search_input = ''
		



	def __check_item(self,c:Command):
		for sc in c.cmd_keys:
			if sc in self.commandline_keys:
				print(f'{sc} {c} already in cmd_keys !')
				continue
			self.commandline_keys[sc] = c
		return True
	
	def append(self,*ar:List[Command]):
		for v in ar:
			if not self.__check_item(v):
				continue
			super().append(v)
		
	def __getitem__(self, index)->Command:
		return super().__getitem__(index)
	
	def __setitem__(self, key, v:Command):
		if not self.__check_item(v):
			return
		return super().__setitem__(key, v)


	
	def set_items_filtered(self):
		def get() -> List[Command]:
			if not self.searching:
				return self
			if not self.search_input:
				return self


			def search_filter_and(x:Command):
				nl = x.name.lower()
				for a in self.search_input.lower():
					if a and (nl.find(a) == -1):
						return False
				return True
			
			def search_filter(x:Command):
				return x.name.lower().find(self.search_input.lower()) != -1
			
			return list(filter(search_filter_and,self))

		self.items_filtered = get()
	



	@property
	def items_to_print(self) -> List[ItemToPrint]:
		self.set_items_filtered()

		row_number = 0
		for result_number in range(self.first_index,self.last_index+1):
			row_number += 1
			cmd_selected = result_number == self.__selected_index
			cmd = self.items_filtered[result_number]
			
			yield ItemToPrint(row_number=row_number,result_number=result_number,selected=cmd_selected,cmd=cmd)
			#yield row_number,cmd_index,cmd_selected,cmd
		


	@property
	def first_index(self):
		return max(0,self.item_start_index)
	
	@property
	def last_index(self):
		return min(len(self.items_filtered) - 1, self.first_index + self.max_rows - 1)


	@property
	def selected_index(self):
		return self.__selected_index

	@selected_index.setter
	def selected_index(self,new_value):
		last_value = self.__selected_index
		new_value  = min(max(0,new_value ), len(self.items_filtered) - 1)
		delta_selected_index = (new_value - last_value)

		if delta_selected_index == 0:
			return
		elif delta_selected_index == 1:
			#one down
			if (self.last_index == last_value):
				self.item_start_index += 1
		elif delta_selected_index == -1:
			#one up
			if (self.first_index == last_value):
				self.item_start_index -= 1
		else:

			self.item_start_index = min(max(0,new_value - math.floor(self.max_rows/2)),max(0,len(self.items_filtered) - self.max_rows))
		
		self.__selected_index = new_value

	@property
	def selected_cmd(self) -> Command:
		try:
			x = self.items_filtered[self.selected_index]
			return x
		except:
			return None
		
class Menu:
	title:str=''
	def __init__(self,*commands : List[Command],start=False,title=None,max_rows=20):
		
		self.title = title
		self.__on_key = dict()
		self.cmds  = Commands(*commands,max_rows=max_rows)



		@self.key('f2')
		def search(menu:Menu):
			menu.cmds.searching = not menu.cmds.searching
			

		
		@self.key('up')
		def up(menu:Menu):
			menu.cmds.selected_index -= 1
			
		@self.key('ppage')
		def up(menu:Menu):
			menu.cmds.selected_index -= menu.cmds.max_rows

		@self.key('npage')
		def down(menu:Menu):
			menu.cmds.selected_index += menu.cmds.max_rows

		@self.key('down')
		def down(menu:Menu):
			menu.cmds.selected_index += 1

		@self.key('enter')
		def enter(menu:Menu):
			if not (cmd := menu.cmds.selected_cmd):
				return
			cmd.exec(menu,cmd)



		

		if start:
			self.start()

	def key(self,keyname):
		if keyname in codeToName:
			keyname = codeToName[keyname]

		

		
	
		if not keyname in nameToCode:
			print(f'Invalid keyname {keyname}')
			exit()
		
		def decorator(f):
			self.__on_key[keyname] = f
			return f
		return decorator
	


	def start(self):
		self.cmds.load_key_listeners(menu=self)
		def wrapper(stdscr):
			C = Curses(stdscr)
			def printer():
				C.clear()

				if self.title:
					C.line(self.title,underline=True)
					C.emptyLine(2)

				for item in self.cmds.items_to_print:
					C.line(item.cmd.name,selected=item.selected,prefix=f'{str(item.result_number).zfill(2)} {str(item.row_number).zfill(2)}   ')
					
				if self.cmds.searching:
					C.emptyLine(2)
					C.line(f'#results : {len(self.cmds.items_filtered)}')
					C.line(f'Searching : {self.cmds.search_input}',add_line_break=False)
					

				userInput = C.wait_for_input()

				if self.cmds.searching and (userInput.c) and (not userInput.name):
					self.cmds.search_input = self.cmds.search_input + userInput.c
					
				else:

				
					if func := self.__on_key.get(userInput.name,None):
						func(self)
					else:
						print(userInput)

			while True:
				printer()

		
		curses.wrapper(wrapper)

	
	def command(self,name,desc=None,cmd_keys=None,exit_after=False,with_parameters=False):
		def decorator(f):
			self.cmds.append(Command(name,f,desc=desc,cmd_keys=cmd_keys,exit_after=exit_after,with_parameters=with_parameters))
			return f
		return decorator

	
