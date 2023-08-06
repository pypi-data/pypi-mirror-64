from typing import List,Dict
from typing import TypeVar, Generic
from logging import Logger

T = TypeVar('T')

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

			
class Event:
	__callbacks : List[CB]
	_is_single  : bool     = False
	_running    : bool     = False

	def __init__(self):
		self.__callbacks = []
	def before_fire(self,*a,**b):
		pass

	def fire(self,*a,**b):
		self._running = True
		self.before_fire(*a,**b)
		for cb in sorted(self.__callbacks,key=lambda x : x.options.priority):
			if self._running:
				cb(self)
			else:
				break
	
	
	def stopPropagation(self):
		self._running = False
	

	@property
	def cb(self):
		return CBOptions().set
	
	def register(self,options:CBOptions=CBOptions(),func=None):
		def add_func(f):
			cb = CB(f,options)
			if self._is_single:
				self.__callbacks = [cb]
			else:
				self.__callbacks.append(cb)
			return f
		if func:
			return add_func(func)
		
		return add_func

class SingleEvent(Event):
	_is_single   : bool     = True



class EventWithKey:
	__keys     : Dict[str,Event] = dict()
	eventClass : Event           = Event
	_is_single  : bool    		 = True
	def __init__(self,eventClass=Event,format_key=None,valid_key=None):
		self.__keys               = dict()
		self.eventClass           = eventClass
		self.eventClass._is_single = self._is_single
		if format_key:
			self.format_key = format_key
		if valid_key:
			self.valid_key = valid_key
		
	@property
	def cb(self):
		return CBOptions().set
	
	def format_key(self,inp):
		return inp
	
	def valid_key(self,key):
		return True

	def get(self,key):
		key = self.format_key(key)
	
		if key in self.__keys:
			return self.__keys[key]
		if self.valid_key(key):
			self.__keys[key] = self.eventClass()
			return self.__keys[key]

	def fire(self,key,*a,**b):
		x = self.get(key)
		if not x:
			return
		x.fire(*a,**b)

	def register(self,key,options:CBOptions=CBOptions(),func=None):
		if ev := self.get(key):
			return ev(options,func=func)



class SingleEventWithKey(EventWithKey):
	_is_single = True

