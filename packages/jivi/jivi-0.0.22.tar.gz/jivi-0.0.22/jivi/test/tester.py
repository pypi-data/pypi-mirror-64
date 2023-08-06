from ..util import String
import traceback

class Tester:
	
	@property
	def classname(self):
		return self.__class__.__name__
	
	@classmethod
	def do(cls):
		c = cls()
		classname = c.classname
		retvals = []

		for testsection in filter(lambda k : not k in dir(Tester), dir(cls)):
			for f in getattr(c,testsection)():
				retval_el = [classname,testsection,f.__name__]
				try:
					resp = f()
					if resp is not None:
						retval_el += ["Failed",resp]
					else:
						retval_el += ["Succes",""]

					retvals.append(retval_el)
				except:
					print(traceback.format_exc())
					retval_el += ["Failed",traceback.format_exc()]

		for a in String.same_len_ar(retvals):
			print(a)

from time import time

class PerformanceTest:
	def __init__(self,*funcs):
		self.funcs = funcs
	def run(self,runs=500,*a,**b):
		ar = []
		for f in self.funcs:
			ar_el = [f.__name__]
			s = time()
			for i in range(runs):
				f(*a,**b)
			
			ar_el.append(time() - s)
			ar.append(ar_el)

		for a in String.same_len_ar(ar):
			print(a)

