import math,os,subprocess
import random 								as _random
from datetime 		import 	datetime
from typing 		import 	List
from urllib.request import 	Request, urlopen
from _thread 		import 	start_new_thread as Thread

random_el = _random.choice


def index_random(ar):
	return _random.randint(0,len(ar) - 1)
def enumerate_random(ar):
	i_random = index_random(ar)
	return i_random,ar[i_random]

def enumerate_reversed(ar):
	return [[i,ar[i]] for i in indexes_reversed(ar)]



def indexes_reversed(ar):

	return [i for i in range(len(ar) -1, -1, -1)]


def indexes(ar):

	return [i for i in range(len(ar) -1, -1, -1)]


def fill_to_len(s:str,min_len:int,filler=' ',left_side=True):
	if len(s) >= min_len:
		return s
	if left_side:
		return filler*(min_len - len(s)) + s
	return s + filler*(min_len - len(s))

def between(s:str,a:str,b:str) -> str:
	try:
		x = s.find(a)
		y = s.find(b,x+len(a))
		retval = s[x+len(a):y]
		return retval
	except:
		return None

def random(n=10):
	letters = 'abcdefghijklmnopqrstuvwxyz0123456789'
	return ''.join(_random.choice(letters) for i in range(n))

def same_len_ar(ar,to_string=True):
	max_lens = []
	for i,a in enumerate(ar):
		if not i:
			max_lens = [len(a_el) for a_el in a]
		else:
			max_lens = [max(max_lens[a_ind],len(a[a_ind])) for a_ind in range(len(a))]
	
	ret_val = []
	for x in ar:
		ret_val.append(' '.join([fill_to_len(s,min_len=max_lens[index],left_side=False) for index,s in enumerate(x)]))
	return ret_val

def copy_tab(t):
	return {k : v for k,v in t.items()}

def properties_keys_tab(ob):
	return {k : True for k in ob.__dict__.keys()}

def properties_keys_ar(ob):
	return list(ob.__dict__.keys())

def properties_set_all(ob,proptabtoset=None,**t):
	if t:
		proptabtoset = t
	
	if proptabtoset:
		for k,v in proptabtoset.items():
			setattr(ob,k,v)


def is_str_list(val):
	if not isinstance(val,list):
		return False

	for x in val:
		if not isinstance(x,str):
			return False
	return True


'''
class A:
	vv = ['a']

class B(A):
	vv = ['b']

class C(B):
	vv = ['c']


class D(C):
	vv = ['d']

=> ['d','c','b','a']

'''
def get_value_stack_from_supers(ob,propname,unique=False):
	retval = getattr(ob,propname,[])
	for c in ob.__class__.__mro__:
		x = super(c,ob)
		if hasattr(x,propname):
			retval += getattr(x,propname)
		else:
			break
	
	return set(retval) if unique else retval
		
def download_html(url,get_body=True):
	def getBody(txt):
		body = txt
		try:
			tl = txt.lower()
			a = tl.find('<body')
			b = tl.find('>',a+1)
			c = tl.find('</body>',b)
			body = txt[b+1:c]
		except:
			pass
		return body
	user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'
	headers = { 'User-Agent' : user_agent }
	req = Request(url, None, headers)
	resp = urlopen(req)

	html = resp.read()
	try:
		txt = html.decode()
		return getBody(txt) if get_body else txt
	except:
		return html

def Popen(s):
	try:
		process = subprocess.Popen(s, stdout=subprocess.PIPE,shell=1)
		stdout, stderr = process.communicate()
		if stderr: print(stderr)
		
		stdout = stdout.decode("cp850")
		for x in stdout.splitlines():
			yield x.strip()
	except:
		pass
	
def Pause():
	os.system("pause")

def Clearterminal():
	os.system("cls")

class to_string:
	__BYTE_HELPER = [[math.pow(1024,i),name] for i,name in enumerate(["bytes","KB","MB","GB","TB"])]
	__BYTE_HELPER.reverse()
	@classmethod
	def bytes(cls,number_of_bytes):
		number_of_bytes = float(number_of_bytes)
		if not number_of_bytes:
			return "0 bytes"
		for a in cls.__BYTE_HELPER:
			n = number_of_bytes/a[0]
			if n >= 1:
				return "{a} {b}".format(a=round(n,2),b=a[1])
	@classmethod
	def sec(cls,s):
		h = math.floor(s/3600)
		s -= h*3600
		m =  math.floor(s/60)
		s -= m*60
		return "%02d:%02d:%02d" % (h,m,s)

	@classmethod
	def unix(cls,i):
		return datetime.utcfromtimestamp(i).strftime('%Y-%m-%d %H:%M:%S')


def to_int(n):
	try:
		retval = int(n)
		return retval
	except:
		return None

def good_list_index(index,len_ar):
	return max(0, min(index, len_ar - 1))

def all_true(funcs:List[callable],*a,**b):
	for f in funcs:
		if not f(*a,**b):
			return False
	return True

def first_item(condition,ar:List[any]):
	for i in range(len(ar)):
		if condition(ar[i],i):
			return ar[i]

def first_index(condition,ar:List[any]):
	for i in range(len(ar)):
		if condition(ar[i],i):
			return i
	return None

def cb_func(*a,**b):
	print(f"a : {a}")
	print(f"b : {b}")

def convert_func(func,no_error:bool=False,condition=None,no_para:bool=False):
	t = {k : v for k,v in locals().items() if k != "func"}
	
	if t.get('no_error',False):
		t['no_error'] = False
		def ret_val(*a,**b):
			try:
				ret = func(*a,**b)
				return ret
			except:
				pass
		return convert_func(ret_val,**t)
	if t.get('condition',None):
		condition_func = t.get("condition")
		
		def ret_val(*a,**b):
			if condition_func(*a,**b):
				ret = func(*a,**b)
				return ret
		t['condition'] = None
		return convert_func(ret_val,**t)

	if t.get('no_para',None):
		t['no_para'] = False
		def ret_val(*a,**b):
		
			ret = func()
			return ret

		return convert_func(ret_val,**t)
	


	return func

def convert_func_no_error(f):
	def ret_func(*a,**b):
		try:
			retval = f(*a,**b)
			return retval
		except:
			pass

	return ret_func

def convert_func_condition(f,condition):
	def ret_func(*a,**b):
		if condition(*a,**b):
			return f(*a,**b)
	
	return ret_func

def convert_func_strip_para(f):
	def ret_func(*a,**b):
		return f()
	
	return ret_func

def convert_func_args_kwargs(f,args,kwargs):
	def ret_func():
		return f(*args,**kwargs)
	
	return ret_func


def ar_flatten(ar):
	new_ar = []
	for x in ar:
		new_ar += x

	return new_ar



def convert_func_pff(func,no_error:bool=False,condition=None,no_para:bool=False,kwargs=dict(),args=[]):
	ret_func = func
	if no_error:
		ret_func = convert_func_no_error(ret_func)

	if condition:
		ret_func = convert_func_condition(ret_func,condition)

	if no_para:
		ret_func = convert_func_strip_para(ret_func)


	ret_func = convert_func_args_kwargs(ret_func,args,kwargs)

	return ret_func
	
import sys


def export(fn):
	mod = sys.modules[fn.__module__]
	if hasattr(mod, '__all__'):
		mod.__all__.append(fn.__name__)
	else:
		mod.__all__ = [fn.__name__]
	return fn

#									blabla packed

class Ob:
	properties_set_all  = properties_set_all
	properties_keys_ar  = properties_keys_ar
	properties_keys_tab = properties_keys_tab



class String:
	same_len_ar = same_len_ar
	random  	= random
	between 	= between
	fill_to_len = fill_to_len

class Index:
	first_index 	= first_index
	first_item  	= first_item
	all_true 		= all_true
	good_list_index = good_list_index
	

	@staticmethod
	def first_index_without_index(condition,ar:List[any]):
		for i in range(len(ar)):
			if condition(ar[i]):
				return i
		return None
	@staticmethod
	def first_item_without_index(condition,ar:List[any]):
		for i in range(len(ar)):
			if condition(ar[i]):
				return ar[i]
