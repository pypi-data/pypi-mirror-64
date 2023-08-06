from .models import copy_tab
from .inputparameters import InputParameter
from . import ValueGetter
from .base import UIInput as base


class UIInput(base.UIInput):
	para : InputParameter
	_method_classes : List[callable] = []
	def __init__(self,para : InputParameter):
		self.para = para

	@property
	def my_replacement_tab(self):
		return dict()
	
	@property
	def replacement_tab(self):
		tab = copy_tab(self.para.replacement_tab)
		tab.update(self.my_replacement_tab)
		return tab
	
	@property
	def inputMethods(self):
		return [cls(self) for cls in self._method_classes]
	
	def __repr__(self):
		return f"[<{self.__class__.__name__}>] {self.para}"

class File(base.File):
	_method_classes = [ValueGetter.Filepath,ValueGetter.FileSelecter]

class Json(base.Json):
	_method_classes = [ValueGetter.Filepath,ValueGetter.FileSelecter,ValueGetter.Text]

class Text(base.Text):
	_method_classes = [ValueGetter.Filepath,ValueGetter.FileSelecter,ValueGetter.Text]

class String(base.String):
	_method_classes = [ValueGetter.String]

class Number(base.Number):
	_method_classes = [ValueGetter.Number]