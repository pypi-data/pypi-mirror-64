from __future__ import annotations
from typing import List
import inspect
from jivi import jvUtil


def print_shit(*a:List[any]):
	print('-------------')
	for x in a:
		print(x)
	print('-------------\n')




metaDataPropertyName = '_jvMeta'
logPropertyName = 'jvlog'

def do_log(self,level:str,*inp:List[any]):

	to_print = [f'[{self.parent.__class__.__name__} - {level}]'] + [str(self)] +  [str(x) for x in inp]
	print("\n".join(to_print))

class WrapperLogging:
	def __init__(self,jvMeta : WrapperMetaData, parentObject : object):
		self.jvMeta = jvMeta
		self.parent = jvMeta.parent
		self.parent = parentObject
		#print_shit('parentObject',parentObject)
		
		setattr(self.parent,logPropertyName,self)




	def debug(self,*inp:List[any]):
		#return do_log()
		return self.__do_log('debug',*inp)

	def info(self,*inp:List[any]):
		return self.__do_log('info',*inp)

	def warning(self,*inp:List[any]):
		return self.__do_log('warning',*inp)

	def error(self,*inp:List[any]):
		return self.__do_log('error',*inp)

	def critical(self,*inp:List[any]):
		return self.__do_log('critical',*inp)

	def __do_log(self,level:str,*inp:List[any]):

		to_print = [f'[{self.jvMeta.parent.__class__.__name__} - {level}]'] + [str(self.parent)] +  [str(x) for x in inp]

		print_shit('parentObject',"\n".join(to_print))


		#	print("\n".join(to_print))


	def __repr__(self):
		return f'[WrapperLogging]'
	
class WrapperMetaData:
	parent : object
	to_print : List[str]

	def __init__(self,parent):
		self.parent = parent
		self.to_print = []
		self.to_print_ignore_tab = dict()
		self.print_func_tab = dict()
		setattr(parent,metaDataPropertyName,self)

		

	def add_print_method_names(self,*method_names):
		for method_name in method_names:
			self.print_func_tab[method_name] = True	
			self.add_propnames_to_skip(getattr(getattr(self.parent,method_name,{}),'propnames_to_skip',[]))
			
			

	def add_propnames_to_skip(self,propnames_to_skip:List[str]=[]):
		for propname_to_skip in propnames_to_skip:
			self.to_print_ignore_tab[propname_to_skip] = True

	def init_print_funcs(self):
		self.add_print_method_names(*[method_name for method_name, method in self.parent.__dict__.items() if hasattr(method, "print_func")])

		
		
		metaData = self
		def replace_method(method_name):
			old_method = getattr(self.parent,method_name,None)
			if old_method is None:
				print(f'old_method is none {method_name}')
				return None
			
			def replacement(self,*a,**b):
				old_keys = jvUtil.ob.properties_keys_tab(self)
				
				

				if method_name == '__init__':
					WrapperLogging(metaData,self)
					
				retval = old_method(self,*a,**b)
				metaData.add_to_print(
					new_properties := [propname for propname in jvUtil.ob.properties_keys_ar(self) if not propname in old_keys]
				)
				return retval
	
			return replacement

		for method_name in self.print_func_tab.keys():
			setattr(self.parent,method_name,replace_method(method_name))

	def add_to_print(self,ar):
		for x in filter(lambda el : el not in self.to_print_ignore_tab,ar):
			self.to_print_ignore_tab[x] = True
			self.to_print.append(x)

	def class_to_string(self,ob):
		to_print_ar = [[f'[{self.parent.__name__}]','','']]
		for k in self.to_print:
			s_key = str(k)
			s_val = str(getattr(ob,k,None))
			to_print_ar.append(['',s_key,s_val])
		
		max_lens = []
		for i,a in enumerate(to_print_ar):
			if not i:
				max_lens = [len(a_el) for a_el in a]
			else:
				max_lens = [max(max_lens[a_ind],len(a[a_ind])) for a_ind in range(len(a))]

		to_print_ar_next_step = []

		for ar in to_print_ar:
			to_print_ar_next_step.append(' '.join([jvUtil.string.fill_to_len(s,min_len=max_lens[index],left_side=False) for index,s in enumerate(ar)]))
		
		return "\n".join(to_print_ar_next_step)

	@classmethod
	def get_meta_data(cls,ob,create=False) -> WrapperMetaData:
		if (ret_val := getattr(ob,metaDataPropertyName,None)) is not None:
			return ret_val
		
		if create:
			
			return WrapperMetaData(ob)
		return None
	

class jvWrapperSuper:
	_jvMeta:WrapperMetaData
	jvlog : WrapperLogging


	


def Wrapper(propnames_to_skip:List[str]=[]):
	def method_decorator(view):
		view.print_func = True
		view.propnames_to_skip = propnames_to_skip
		return view

	def class_decorator(old_class):
		if WrapperMetaData.get_meta_data(old_class):
			return old_class

		data = WrapperMetaData.get_meta_data(old_class,create=True)
		data.add_print_method_names('__init__')
		data.add_propnames_to_skip(propnames_to_skip)
		data.init_print_funcs()

		class JivfoWrapperClass(old_class):
			_jvMeta:WrapperMetaData
			jvlog : WrapperLogging
			def __repr__(self):
				return self._jvMeta.class_to_string(self)

		return JivfoWrapperClass

	def decorator(old):
		return class_decorator(old) if inspect.isclass(old) else method_decorator(old)
	
	return decorator
