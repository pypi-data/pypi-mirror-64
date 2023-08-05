from . import string
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
					retval_el += ["Failed",traceback.format_exc()]

		for a in string.same_len_ar(retvals):
			print(a)
