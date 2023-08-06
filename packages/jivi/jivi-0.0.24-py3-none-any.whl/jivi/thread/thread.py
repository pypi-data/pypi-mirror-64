import threading,traceback,math
from typing import List
from time import time,sleep

def get_tab_from_locals(loc):
	return {k : v for k,v in loc.items() if k != 'self'}


class ThreadOptions:
	time_delta : int = None
	"""
	dynamic_time : next run will be at (interval/sleep_time - runtime)
	"""
	def __init__(self,
			interval        : int  = None,
			start_with_wait        = False,
			dynamic_time           = False,
			condition              = None,
			daemon                 = True,
			sleep_time      : int  = None,
			no_loop         : bool = False,
			debug           : bool = False,
			first_run:callable=None):

		self.set(**get_tab_from_locals(locals()))
	"""
	dynamic_time : next run will be at (interval/sleep_time - runtime)
	"""
	def set(self,
			interval        : int  = None,
			start_with_wait        = False,
			dynamic_time           = False,
			condition              = None,
			daemon                 = True,
			sleep_time      : int  = None,
			no_loop         : bool = False,
			debug           : bool = False,
			first_run:callable=None):
		
		for k,v in get_tab_from_locals(locals()).items():
			setattr(self,k,v)

		
		return self
	



	

class ThreadOptionsHelper_old:
	def __init__(self,ops:ThreadOptions):
		self.interval	     = ops.interval
		self.start_with_wait = ops.start_with_wait
		self.dynamic_time    = ops.dynamic_time
		self.condition		 = ops.condition
		self.daemon			 = ops.daemon
		self.sleep_time		 = ops.sleep_time
		self.time_delta		 = self.interval if self.interval is not None else (self.sleep_time if self.sleep_time is not None else None)



	def set_start_time(self):
		self._start_time = time()
	
	def sleep_first_time(self):
		if self.time_delta is None:
			return None
	def sleep(self):
		if not self.time_delta:
			return
		
		stop_time = time()
		time_to_sleep = max(0,self.time_delta - ( stop_time - self._start_time )) if self.dynamic_time else self.time_delta
		self._start_time = stop_time
		if not time_to_sleep:
			return
		sleep(time_to_sleep)

	

class ThreadOptionsHelper:
	def __init__(self,ops:ThreadOptions,func=None,args=[],kwargs=dict()):
		self.ops 			 = ops
		self.time_delta		 = self.ops.interval if self.ops.interval is not None else (self.ops.sleep_time if self.ops.sleep_time is not None else None)
		self.func 			 = func
		self.args 			 = args
		self.kwargs 		 = kwargs
	
		self.start()
	
	def info(self,*a):
		if not self.ops.debug:
			return
		print(f'Thread {self.func.__name__}',*a)
	def start(self):

		def thread_function(*a,**b):

			t = threading.currentThread()
			def condition_func(*a,**b):
				if not getattr(t,'is_running',True):
					print('stopped running!')
					return False
				if self.ops.condition:
					return self.ops.condition(*a,**b)
				return True
		
			if self.ops.first_run:
				self.ops.first_run(*a,**b)
			self.sleep_first_time()
			self._start_time = time()
			while condition_func(*a,**b):
			
				self.func(*a,**b)
				self.sleep()
				if self.ops.no_loop:
					break
				self._start_time = time()
		
		t = threading.Thread(target=thread_function,args=self.args,kwargs=self.kwargs,daemon=self.ops.daemon)
		setattr(t,"is_running",True)
		t.start()

					
	
	def sleep_first_time(self):
		if self.time_delta is None:
			return None
		if self.ops.start_with_wait:
			sleep(self.time_delta)
	def sleep(self):
		if not self.time_delta:
			return
		
		
		stop_time = time()
	
		time_to_sleep = max(0,self.time_delta - ( stop_time - self._start_time )) if self.ops.dynamic_time else self.time_delta

		if not time_to_sleep:

			return
		sleep(time_to_sleep)
	
class ThreadClass:

	@property
	def options(self):
		return ThreadOptions().set

	@staticmethod
	def conditionProp(ob,propname,eq=True,neq=None):
		def ret_func(*a,**b):
			val = getattr(ob,propname)
			if eq is not None:
				return val == eq
			if neq is not None:
				return val != neq
			return False
		return ret_func
	
	def register(self,options:ThreadOptions=ThreadOptions(),func=None,args=[],kwargs=dict()):
		if func:
			return ThreadOptionsHelper(options,func=func,args=args,kwargs=kwargs)
		
		def add_func(f):
			ThreadOptionsHelper(options,func=f,args=args,kwargs=kwargs)
			return f
		
		return add_func
	
	def register_old(self,options:ThreadOptions=ThreadOptions(),func=None,args=[],kwargs=dict()):
		helper = ThreadOptionsHelper(options)
		def add_func(f):
			def func(*a,**b):
				t = threading.currentThread()
				def condition_func(*a,**b):
					if not getattr(t,'is_running',True):
						print('stopped running!')
						return False
					if options.condition:
						return options.condition(*a,**b)
					return True
				
				helper.sleep_first_time()
				helper.set_start_time()
				while condition_func(*a,**b):
					
					f(*a,**b)
					
					helper.sleep()
					if options.no_loop:
						break
				
			t = threading.Thread(target=func,args=args,kwargs=kwargs,daemon=options.daemon)
			setattr(t,"is_running",True)
			t.start()
			
			return f
		
		if func:
			return add_func(func)
		
		return add_func

	@classmethod
	def stop_all(cls,max_wait_for_it:int=0):
		print(f'stop all started {len(threading.enumerate())}')
		
		for t in threading.enumerate():
			try:
				setattr(t,'is_running',False)
				t.join(0.1)
			except:
				pass
		
		if max_wait_for_it:
			max_time   = time() + max_wait_for_it
			while time() < max_time:
				if not threading.activeCount():
					return True
				sleep(0.1)
			print(threading.activeCount())
			return False
		else:
			return not threading.activeCount()
		

				
					



Thread = ThreadClass()


