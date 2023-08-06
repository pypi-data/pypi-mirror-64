from typing import List

class CBOptions:
	clear_args : bool     	= False
	add_args   : List[any]	= []
	add_kwargs : dict     	= dict()
	condition  : callable 	= None
	no_error   : bool     	= False
	priority   : int		= 2
	def __init__(self,
				priority 			   = 2,
				clear_args             = False,
				add_args               = [],
				add_kwargs             = dict(),
				condition              = None,
				no_error			   = False):
		self.set(priority=priority,clear_args=clear_args,add_args=add_args,add_kwargs=add_kwargs,condition=condition,no_error=no_error)
	
	def set(self,priority=priority,clear_args= False,add_args= [],add_kwargs= dict(),condition=None,no_error=False):
		self.priority   = priority
		self.clear_args = clear_args
		self.add_args   = add_args
		self.add_kwargs = add_kwargs
		self.condition  = condition
		self.no_error   = no_error
		return self
	
	@property
	def copy(self):
		return self.__class__(priority=self.priority,clear_args=self.clear_args,add_args=self.add_args,add_kwargs=self.add_kwargs,condition=self.condition,no_error=self.no_error)


class CB:
	def __init__(self,func : callable,options:CBOptions=CBOptions()):
		self.original_func = func
		self.func          = self.original_func
		self.options       = options
		if options.condition:
			self.__convert_condition(options.condition)
		if options.no_error:
			self.__convert_no_error()
	
	def __convert_condition(self,condition):
		f = self.func
		def new_func(*a,**b):
			if condition(*a,**b):
				return f(*a,**b)
		self.func = new_func

	def __convert_no_error(self):
		f = self.func
		def new_func(*a,**b):
			try:
				retval = f(*a,**b)
				return retval
			except:
				pass
		self.func = new_func
	
	def __call__(self,*a,**b):
		if self.options.clear_args:
			return self.func(*self.options.add_args,**self.options.add_kwargs)
		else:
			for k,v in self.options.add_kwargs.items():
				b[k] = v
			return self.func(*a,*self.options.add_args,**b)