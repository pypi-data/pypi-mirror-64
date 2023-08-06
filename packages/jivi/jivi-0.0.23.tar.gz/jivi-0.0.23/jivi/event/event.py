from typing import TypeVar, Generic,List,Dict
from typing import Callable

from logging import Logger
from ..callback import *


T = TypeVar('T')


class Event:
	__callbacks : List[CB]
	_is_single  : bool     = False
	_running    : bool     = False
	def __init__(self,single=False,before_fire=None):
		self._is_single  = single
		self.__callbacks = []
		if before_fire:
			self.before_fire = before_fire
		
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
		def add_func(f: Callable[[self.__class__],None]) -> Callable[[self.__class__],None]:
			cb = CB(f,options)
			if self._is_single:
				self.__callbacks = [cb]
			else:
				self.__callbacks.append(cb)
			retval : Callable[[self.__class__],None] = f
			return retval
		
		if func:
			return add_func(func)
		
		return add_func
	def __call__(self,options:CBOptions=CBOptions(),func=None):
		return self.register(options,func=func)

class EventWithParent(Event,Generic[T]):
	parent   : T
	def __init__(self,single=False,before_fire=None,parent:T=None):
		super().__init__(single=single,before_fire=before_fire)
		self.parent = parent


class EventWithKey:
	__events     : Dict[str,Event] = dict()
	eventClass   : Event           = Event
	_is_single   : bool            = True
	_before_fire : callable        = None
	def __init__(self,single=False,eventClass=Event,format_key=None,valid_key=None,before_fire=None):
		self.__events   = dict()
		self.eventClass = eventClass
		self._is_single = single
		if format_key:
			self.format_key = format_key
		if valid_key:
			self.valid_key = valid_key
		
		self._before_fire = before_fire

	@property
	def cb(self):
		return CBOptions().set
	
	def format_key(self,inp):
		return inp
	
	def valid_key(self,key):
		return True

	def _create(self):
		return self.eventClass(single=self._is_single,before_fire=self._before_fire)

	def get(self,key):
		key = self.format_key(key)
		if key in self.__events:
			return self.__events[key]
		if self.valid_key(key):
			self.__events[key] = self._create()
			return self.__events[key]

	def fire(self,key,*a,**b):
		x = self.get(key)
		if not x:
			return
		x.fire(*a,**b)

	def register(self,key,options:CBOptions=CBOptions(),func=None):
		if ev := self.get(key):
			return ev.register(options,func=func)

class EventWithKeyWithParent(EventWithKey,Generic[T]):
	parent   : T
	__events     : Dict[str,EventWithParent[T]] = dict()

	def __init__(self,single=False,eventClass=EventWithParent[T],format_key=None,valid_key=None,before_fire=None,parent:T=None):
		super().__init__(single=single,eventClass=eventClass,format_key=format_key,valid_key=valid_key,before_fire=before_fire)
		self.parent = parent

	def _create(self):
		return self.eventClass(single=self._is_single,before_fire=self._before_fire,parent=self.parent)
	