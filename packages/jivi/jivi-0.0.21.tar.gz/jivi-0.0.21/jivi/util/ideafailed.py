
def kw_or_self(f:callable):
	named_arguments = list(f.__code__.co_varnames[len(f.__code__.co_varnames)-len(f.__defaults__):])
	def retval(self,*a,**b):
		for k in filter(lambda x : (b.get(x,None) is None) and hasattr(self,x), named_arguments):
			b[k] = getattr(self,k)
		f(self,*a,**b)
	return retval


def key_list_not_null(t):
	return ','.join([k for k,v in t.items() if v is not None])

def ob_set(f:callable=None,kw_or_self=None):
	
	if f is not None:
		named_arguments = {k : f.__defaults__[ix] for ix,k in enumerate(f.__code__.co_varnames[len(f.__code__.co_varnames)-len(f.__defaults__):])}
		fstr = str(f)

		do_print = fstr.find("Box") != -1
		if do_print:
			print("varnames",f.__code__.co_varnames)
			print("varnames len",len(f.__code__.co_varnames))
			print("defaults len",len(f.__defaults__))
			print("defaults",f.__defaults__)
			print("named_arguments",named_arguments)
			print("named_arguments len",len(named_arguments))
		def retval(self,*a,**b):
			if do_print:
				print(self.__class__.__name__,named_arguments)
			#print("b",key_list_not_null(b))
			#print(f.__name__,self,a,b)
			if kw_or_self:
				for k in filter(lambda x : (b.get(x,None) is None) and hasattr(self,x), named_arguments):
					b[k] = getattr(self,k)
			bb = {k : b.get(k,v) for k,v in named_arguments.items()}
			if do_print:
				print(self.__class__.__name__,"bb",bb)
			for k,v in bb.items():
				setattr(self,k,v)
			f(self,*a,**b)
		return retval
	else:
		def retval(f,kw_or_self=kw_or_self):
			return ob_set(f,kw_or_self=kw_or_self)
		return retval

def ob_init_props(ob,locs,not_none=True):
	for k,v in locs.items():
		if k == "self":
			continue
		if not_none and v is None:
			continue
	
		setattr(ob,k,v)
