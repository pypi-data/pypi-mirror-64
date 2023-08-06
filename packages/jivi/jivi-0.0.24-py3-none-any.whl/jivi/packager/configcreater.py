from ..wrapper 	import jvWrapper,jvWrapperSuper
from typing 	import List,Dict
from ..fs		import JDir,JFile
from ..uinput	import UInput


inputType = UInput.type

# class ConfigFieldType:
# 	inputType = InputType.string
# 	@classmethod
# 	def is_valid(cls,val):
# 		return isinstance(val,str)

# class ConfigFieldTypeString(ConfigFieldType):

# 	@classmethod
# 	def is_valid(cls,val):
# 		return isinstance(val,str)

# class ConfigFieldTypeFile(ConfigFieldTypeString):
# 	inputType = InputType.file
# 	@classmethod
# 	def is_valid(cls,val):
# 		return super().is_valid(val) and JFile(val).exists

# class ConfigFieldTypeJsonFile(ConfigFieldTypeString):
# 	inputType = InputType.json
# 	@classmethod
# 	def is_valid(cls,val):
# 		return super().is_valid(val) and JFile(val).exists



class ConfigField:
	key 		: str
	inputType 	: UInput.type.Type
	__value     : any

	def __init__(self,inputType,default=None):
		self.__value    = None
		self.inputType  = inputType
		self.default 	= default
	
	def __repr__(self):
		return f"[ConfigField] {self.key}"
	
	def set_value_if_not_set(self,val):
		if self.is_set:
			return
		self.value = val
	
	def try_setting(self):
		val = self.inputType.get_input(self.key)
		
	
	@property
	def value(self):
		if not self.is_set:
			return self.default
		
		return self.__value

	@value.setter
	def value(self,val):
		if self.inputType.is_valid(val):
			self.__value = val
			return
		print(f"Not valid value {val}")
	
	@property
	def is_set(self):
		return self.__value is not None
	

default_classifiers = ["Programming Language :: Python :: 3","License :: OSI Approved :: MIT License","Operating System :: OS Independent"]

@jvWrapper()
class ConfigCreater(jvWrapperSuper):
	name                          						= ConfigField(inputType.String)
	author                        						= ConfigField(inputType.String)
	author_email                  						= ConfigField(inputType.String)
	description                   						= ConfigField(inputType.String)
	long_description              						= ConfigField(inputType.File)
	long_description_content_type 						= ConfigField(inputType.String,default="text/markdown")
	url                           						= ConfigField(inputType.String)
	classifiers 				  						= ConfigField(inputType.JsonFile,default=default_classifiers)

	__all_fields 										= dict()
	def __init__(self,*json_config_files:List[str]):
		self.__all_fields = dict()
		for k,v in map(lambda x : (x,getattr(self,x)),filter(lambda k : isinstance(getattr(self,k),ConfigField),dir(self))):
			self.__all_fields[k] = v
			v.key = k
		
		self.read_from_file(*json_config_files)
		self.set_unset()

	def set_unset(self):
		for k,v in self.fields_not_set.items():
			v.try_setting()
			
	
	@property
	def fields_not_set(self) -> Dict[str,ConfigField]:
		return {k : v for k,v in self.__all_fields.items() if not v.is_set}
			


	
	def read_from_file(self,*filenames:List[str]):
		for filename in filenames:
			jFile = JFile(filename)
			if not jFile.exists:
				self.jvlog.warning(f"Filename {filename} not found!")
				continue
			jTab = jFile.reader.json()
			if not jTab:
				self.jvlog.warning(f"Filename {filename} unable to read json!")
				continue
			for k,v in self.__all_fields.items():
				if k in jTab:
					v.set_value_if_not_set(jTab[k])
			

