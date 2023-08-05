from .models import InputParameter,string_replacer,copy_tab
from . import UIInput
from .base import ValueGetter as base

class Item(base.Item):
	_title_base : str            = "Getvaluefor[name]"
	_desc_base  : str            = "Getvaluefor[name]"
	uiInput     : UIInput.UIInput          
	def __init__(self,uiInput:UIInput):
		self.uiInput = uiInput


	@property
	def para(self):
		return self.uiInput.para
	
	@property
	def desc(self):
		return string_replacer(self._desc_base,self.replacement_tab)

	@property
	def title(self):
		return string_replacer(self._title_base,self.replacement_tab)
	
	@property
	def my_replacement_tab(self):
		return dict()
	
	@property
	def replacement_tab(self):
		tab = copy_tab(self.uiInput.replacement_tab)
		tab.update(self.my_replacement_tab)
		return tab

	def __repr__(self):
		return f"[<{self.__class__.__name__}>] {self.title}"

class FileSelecter(base.FileSelecter):
	_desc_base  = "Browse for [name]"
	_title_base = "Please select file [name]"

class String(base.String):
	_desc_base  = "Input text for [name]"
	_title_base = "Please input [name]"


class Number(base.Number):
	_desc_base  = "Input number for [name]"
	_title_base = "Please input number [name]"


class Filepath(base.Filepath):
	_desc_base  = "Input path to [name]"
	_title_base = "Please the filepath to [name]"


class Text(base.Text):
	_desc_base  = "Input text for [name]"
	_title_base = "Please input [name]"