from . import ValueGetter
from ..models import InputParameter,copy_tab,IHasReplacement_tab
from .. import Validator
from typing import List
from jivi.util.ob import get_value_stack_from_supers

class UIInput(IHasReplacement_tab):
	para            : InputParameter            = None
	_method_classes : List[callable]            = []
	_validators     : List[Validator.Validator] = []

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

	@property
	def validators(self) -> List[Validator.Validator]:
		return [val(self) for val in get_value_stack_from_supers(self,'_validators',True)]

	
class File(UIInput):
	_method_classes = [ValueGetter.Filepath,ValueGetter.FileSelecter]

	@property
	def validators(self) -> List[Validator.Validator]:

		return []
	
class Json(File):
	validators      = [Validator.FileExists]
	_method_classes = [ValueGetter.Filepath,ValueGetter.FileSelecter,ValueGetter.Text]

class Text(UIInput):
	_method_classes = [ValueGetter.Filepath,ValueGetter.FileSelecter,ValueGetter.Text]

class String(UIInput):
	_method_classes = [ValueGetter.String]

class Number(UIInput):
	_method_classes = [ValueGetter.Number]