from __future__ import annotations
from typing import List
from jivi.util.ob import copy_tab
import re
from jivi.fs import JFile
from ..models import IHasReplacement_tab,string_replacer

class Validator:
	_error_text = "[value] is invalid!"
	parent     : IHasReplacement_tab
	validate   : callable
	value	   : any
	def __init__(self,parent:IHasReplacement_tab):
		self.parent = parent

	@property
	def error_text(self):
		return string_replacer(self._error_text,self.parent.replacement_tab,value=self.value)

	def __repr__(self):
		return f"[<{self.__class__.__name__}>] {self.value}"


def __creater(error_text:str):
	def decorator(validate_func) -> Validator:
		class ret_cls(Validator):
			_error_text = error_text
			def validate(self,value):
				self.value = value
				return validate_func(self,value)
		ret_cls.__name__ = validate_func.__name__
		return ret_cls
	return decorator

class StringNotEmpty(Validator):
	_error_text = "[value] is required!"
	def validate(self,value:str):
		return len(value.strip()) > 0
class Email(Validator):
	_error_text = "[value] is not a valid email!"
	def validate(self,value):
		return re.match("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",value)

class FileExists(Validator):
	_error_text = "File [value] does not exist!"
	def validate(self,value):
		return JFile(value).exists
	
class FileHasContent(Validator):
	_error_text = "File [value] has no content or does not exist!"
	def validate(self,value):
		return JFile(value).reader.text

class FileIsJson(Validator):
	_error_text = "File [value] is not a valid json or cant be read!"
	def validate(self,value):
		return JFile(value).reader.json()


@__creater("Is not bigger than 10")
def BiggerThan10(self,value) -> Validator:
	return value > 10




def tester():

	class testparent(IHasReplacement_tab):
		@property
		def replacement_tab(self):
			return dict(name="OMO")
		
	x = BiggerThan10(testparent())

	x.validate(8)
	print(x)
	print(x.error_text)