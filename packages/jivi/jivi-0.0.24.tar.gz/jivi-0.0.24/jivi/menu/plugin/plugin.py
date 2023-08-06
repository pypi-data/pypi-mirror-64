import curses, curses.ascii, traceback
from curses.textpad 				import Textbox, rectangle
from typing 						import List
from prompt_toolkit.shortcuts 		import input_dialog, message_dialog
from ...fs 							import JDir, JFile
from ...fs.fs 						import JDirFileWrapper
from ...util 						import cb_func
from .. 							import Ctrl, Menu, MenuItem
from .. 							import addon as MenuAddon
from ..addon.addon 					import Addon
from ..menu 						import Button, Ctrl, Curses, InputChar, Menu, MenuItem



class Plugin(Addon):
	pass

class Explorer(Plugin):
	ctrl   : Ctrl 
	menu   : Menu 
	retval : JFile
	running: bool
	def __init__(self,menu_title=None,looking_for:str=None,start_dir=None,filters=[],ex=[],ctrl:Ctrl=None,cb=None):
		super().__init__(ctrl)
		self.start_dir   = JDir.ToJDir(start_dir,JDir.cwd())
		self.filters     = filters
		self.ex          = ex
		self.looking_for = looking_for
		self.menu_title  = menu_title
		self.current_dir = self.start_dir.copyob
		self.retval      = None
		self.ctrl		 = ctrl
		self.running 	 = False
		self.callback    = cb
	
	def display(self):
		self.running = True
		self.start_menu()
		self.build_current_dir()
		self.ctrl.display()

	def get_menu_title(self):
		if self.menu_title:
			return self.menu_title
		if self.looking_for:
			return f"Select file {self.looking_for}"
		return f"Select file"
	
	def start_menu(self):
		if not self.ctrl:
			self.ctrl = Ctrl()
		ctrl = self.ctrl
		MenuAddon.FirstLetter(ctrl)
		MenuAddon.Scrollbar(ctrl)
		MenuAddon.Searchbox(ctrl)
		self.ctrl = ctrl
		self.menu = self.ctrl.create_menu(self.get_menu_title())

		@self.ctrl.on_key("left")
		def on_key_left(ctrl:Ctrl):
			self.current_dir.up()
			self.build_current_dir()

		@self.ctrl.on_key("right")
		def on_key_right(ctrl:Ctrl):
			if ctrl.selected_item and ctrl.selected_item.data.isdir:
				ctrl.do_key("enter")

	def filter(self,el:JDirFileWrapper):
		if el.isdir:
			return True
		for f in self.filters:
			if not f(el):
				return False
		return True

	def build_current_dir(self):
		self.menu.reset()
		menu : Menu = self.menu
		for ob in filter(self.filter,self.current_dir.reader.get(asob=True,deep=False,ex=self.ex)):
			ob : JDirFileWrapper = ob
			@menu.item(text=ob.name,data=ob)
			def ok(mi:MenuItem):
				x : JDirFileWrapper = mi.data
				if x.isdir:
					self.current_dir.fp = x.fp
					self.build_current_dir()
				else:
					def cb(retval:bool):
						before = self.ctrl.active_menu_index
						self.menu.setActive()
						after = self.ctrl.active_menu_index
						if retval:
							self.callback(x)
							self.menu.ctrl.stop()
						else:
							print(f"declined {x.fp}")
					try:
						q = YesNoQuestion("Select this file ?",ctrl=self.ctrl,cb=cb)
					except:
						print(traceback.format_exc())

class LineInput:
	def __init__(self,title:str,text:str,*validator:List[callable],cb:callable=None):
		self.dialog     = input_dialog(title=title,text=text)
		self.validators = validator
		self.cb         = cb
		self.run_dialog()

	@property
	def valid(self):
		for x in self.validators:
			if not x(self.result):
				return False
		return True
	
	def run_dialog(self):
		self.result = self.dialog.run()
		if self.result is None:
			return self.do_callback(cancel=True)
		if self.valid:
			print('valid')
			return self.do_callback()
		self.run_dialog()

	def do_callback(self,cancel=False):
		if not self.cb:
			return
		if cancel:
			self.cb(None)
		else:
			self.cb(self.result)

class SelecterOption:
	def __init__(self,text:str,value:any):
		self.text = text
		self.value = value

class Selecter(Plugin):
	ctrl   : Ctrl 
	menu   : Menu 
	def __init__(self, title:str,*options:List[SelecterOption],ctrl:Ctrl=None,cb:callable=None):
		super().__init__(ctrl)
		self.ctrl  = ctrl if ctrl is not None else Ctrl()
		self.menu = self.ctrl.create_menu(title)

		for op in options:
			@self.menu.item(text=op.text,data=op.value)
			def op_select(mi:MenuItem):
				cb(mi.data)
		
		self.menu.setActive()

class TextInput:
	def __init__(self,title:str,cb:callable,ctrl:Ctrl=None):
		self.title = title
		self.cb    = cb
		self.ctrl  = ctrl if ctrl is not None else Ctrl()
		curses.wrapper(self.display)

	def button_save_clicked(self):
		self.running = False
	
	def display(self,stdscr):
		self.running = True
		cur          = self.ctrl.cur
		max_y        = cur.max_y
		max_x        = cur.max_x
		editwin      = curses.newwin(max_y-6,max_x-2,4,1)
		self.button  = Button("Save",stdscr,self.button_save_clicked,top=0,right=max_x-2)
		rectangle(stdscr, 3, 0, max_y -2, max_x - 1)
		stdscr.refresh()
		box = MyTextbox(editwin,textInput=self)
		while self.running:
			ch = editwin.getch()
			if not ch:
				continue
			if ch == curses.KEY_MOUSE:
				mPos = Curses.get_mouse()
				self.button.handle_click(mPos)
			else:
				inp = InputChar(ch)
				box.proc_key(inp)

		txt = box.gather()
		self.cb(txt)

class MyTextbox(Textbox):
	def __init__(self, *a, textInput : TextInput=None, **b):
		super().__init__(*a,**b)
		self.textInput = textInput
	
	def proc_key(self,inp:InputChar):
		if inp.name == "f2":
			self.textInput.running = False
			return
		if not self.do_command(inp.code):
			self.textInput.running = False
			return
		self.win.refresh()

class YesNoQuestion(Plugin):
	ctrl   : Ctrl 
	menu   : Menu 
	def __init__(self, question:str,ctrl:Ctrl=None,cb:callable=None):
		super().__init__(ctrl)
		self.ctrl  = ctrl if ctrl is not None else Ctrl()
		self.menu = self.ctrl.create_menu(question)
		@self.menu.item(text="Yes",data=True)
		def ok(mi:MenuItem):
			try:
				cb(mi.data)
			except:
				print(traceback.format_exc())
		@self.menu.item(text="No",data=False)
		def ok(mi:MenuItem):
			try:
				cb(mi.data)
			except:
				print(traceback.format_exc())

		self.menu.setActive()