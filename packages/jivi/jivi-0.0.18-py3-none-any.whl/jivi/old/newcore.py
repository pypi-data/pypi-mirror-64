import math
import os
import subprocess
import traceback
import json
import time
import shutil
from _thread import start_new_thread as Thread
perr = traceback.print_exc

class JiviCore:
	DEFAULT_ENCODING = "cp850"

	@classmethod
	def cmd(cls,cmd:str):
		process = subprocess.Popen(cmd, shell = True)
		stdout, stderr = process.communicate()
	
	@classmethod
	def decode(cls,b : bytes,encoding=None) -> str:
		encoding_to_try = ([encoding,cls.DEFAULT_ENCODING] if encoding is not None else [cls.DEFAULT_ENCODING]) + ['cp1252','ascii','utf-8','latin-1']
		for a in encoding_to_try:
			try:
				s = b.decode(a)
				return s
			except:
				pass

	@classmethod
	def popen(cls,s:str,as_gen=True,stripped=True) -> [str]:
		def func():
			try:
				process 		= subprocess.Popen(s, stdout=subprocess.PIPE,shell=1)
				stdout, stderr 	= process.communicate()
				if stderr: 
					print(stderr)
				
				stdout = cls.decode(stdout)
				for x in stdout.splitlines():
					yield x.strip() if stripped else x
			except:
				pass
		if not as_gen:
			return list(func())
		return func()

class JiviDir:
	@classmethod
	def fp(cls,*inp,d=None,with_sep=True):
		
		fp_parts 	= [cls.fp_sepper(x,True) for x in (inp if d is None else [d] + list(inp))]
		fp 			= os.path.join(*fp_parts)
		return cls.fp_sepper(os.path.abspath(fp),with_sep=with_sep)
	
	@classmethod
	def fp_sepper(cls,fp,with_sep=True):
		return fp.rstrip(os.sep) + os.sep if with_sep else fp.rstrip(os.sep)
	
	@classmethod
	def cwd(cls,with_sep=True):
		return cls.fp(os.getcwd(),with_sep=with_sep)
	
	@classmethod
	def ends_with_sep(cls,fp:str):
		return fp.endswith(os.sep)
	
	@classmethod
	def up(cls,fp,n=1):
		return cls.fp(fp + os.sep,('..' + os.sep)*n,with_sep=cls.ends_with_sep(fp))

	@classmethod
	def name(cls,fp):
		return os.path.basename(cls.fp(fp).rstrip(os.sep))
	
	@classmethod
	def rel(cls,fp,b,with_sep=True):
		return cls.fp_sepper(os.path.relpath(fp,b),with_sep)
	
	@classmethod
	def find_file(cls,fp,fn,deep=1):
		flags = ['b','a-d']
		if deep: 
			flags.append('s')
		
		fp    = cls.fp(fp,with_sep=True)
		flags = JiviAr.join_start_too(flags,'/')
		cmd   = f'dir {fp}{fn} {flags} 2>nul'

		return JiviCore.popen(cmd,as_gen=True)

	@classmethod
	def find_dir(cls,fp,name,deep=1):
		fp    = cls.fp(fp,with_sep=True)

		if not deep:
			dp_to_find = cls.fp(fp,name)
			if cls.exists(dp_to_find):
				return [dp_to_find]
			return []
		
		
		flags = JiviAr.join_start_too(['b','ad','s'],'/')

		cmd   = f'dir {fp}{name} {flags} 2>nul'

		return JiviCore.popen(cmd,as_gen=True)
	
	@classmethod
	def files(cls,fp,full=1,ex=['*'],deep=None,img=None):
		if img:
			ex = ['bmp','jpg','jpeg','gif','png']
		fp    = cls.fp(fp,with_sep=True)
		flags = ['b','a-d']

		if deep: 
			flags.append('s')
			full = 0
	

		if isinstance(ex,str):
			ex = [ex]
		
		x 	  = " ".join([f'"{fp}*.{e}"' for e in ex])
		flags = JiviAr.join_start_too(flags,'/')
		cmd   = f'dir {x} {flags} 2>nul'

		for x in JiviCore.popen(cmd,as_gen=True):
			yield fp + x if full else x
		
	@classmethod
	def dirs(cls,fp,full=1,deep=None):
		fp    = cls.fp(fp,with_sep=True)
		flags = ['b','ad']
		if deep: 
			flags.append('s')
			full = 0
	
		flags = JiviAr.join_start_too(flags,'/')
		cmd   = f'dir {fp} {flags} 2>nul'

		for x in JiviCore.popen(cmd,as_gen=True):
			yield fp + x if full else x

	@classmethod
	def exists(cls,fp):
		return os.path.isdir(fp)


	@classmethod
	def create(cls,fp):
		fp = cls.fp(fp)
		JiviCore.cmd('IF NOT EXIST "{fp}" mkdir "{fp}"'.format(fp=fp))
		return fp
		


class JiviFile:
	@classmethod
	def name(cls,fp,ex=False,lower=False):
		retval = os.path.basename(fp)
		if not ex:
			retval = os.path.splitext(retval)[0]
		
		return retval.lower() if lower else retval

	@classmethod
	def fp(cls,*inp,d=None):
		
		fp_parts 	= inp if d is None else [d] + list(inp)
		fp 			= os.path.join(*fp_parts)
		return os.path.abspath(fp)
	

	@classmethod
	def modified(cls,fp):
		try:
			m = os.path.getmtime(fp)
			return m
		except:
			return 0
	
	@classmethod
	def delete(cls,fp):
		try:
			os.remove(fp)
		except:
			traceback.print_exc()
			return None
	
	@classmethod
	def ex(cls,fp,lower=True):
		if lower: 
			return cls.ex(fp,lower=False).lower()
		try:
			return os.path.splitext(fp)[1][1:]
		except:
			return ""
	
	@classmethod
	def dir(cls,fp):
		return JiviDir.fp(os.path.dirname(fp))
	
	@classmethod
	def exists(cls,fp):
		return os.path.isfile(fp)


class JiviIOReader:
	def __init__(self,io):
		self.io = io
	@property
	def fp(self):
		return self.io.fp
	def all(self,mode='r'):
		try:
			with open(self.fp,mode) as f:
				x = f.read()
				return x
		except:
			traceback.print_exc()

	def all_full(self,encoding='utf-8'):
		try:
			with open(self.fp,'r',encoding=encoding) as f:
				x = f.read()
				x = "\n".join(list(x.replace("\r\n", "\n").splitlines()))
	
				return x
		except:
			if encoding == 'utf-8':
				return self.all_full(fp,encoding='cp1252')
			elif encoding == 'cp1252':
				return self.all_full(fp,encoding='mbcs')
		return None
	
	def lines(self,strip=1,encoding='utf-8'):
		try:
			with open(self.fp,'r',encoding=encoding) as f:
				x = [a.rstrip() if strip else a for a in f.readlines()]
				return x
		except:
			pass
		return []
	
	def lines_stripped(self,fp):
		try:
			with open(self.fp,'r') as f:
				x = [a for a in [a.strip() for a in f.readlines()] if a]
				return x
		except:
			pass
		return []
	


	def lines_special(self,fp):
		
		try:
			x = self.all()
			x = x.splitlines()
			return x
		except:
			pass
	
	
	def jsono(self,encoding='utf-8'):
		try:
			with open(self.fp,"r",encoding=encoding) as f:
				s = f.read()
				a = json.loads(s)
				for k in a.keys():
					return a[k]
		except:
			return None
	
	def json(self,encoding='cp1252'):
		try:
			with open(self.fp,"r",encoding=encoding) as f:
				s = f.read()
				a = json.loads(s)
				return a
		except:
			return None



class JiviIOWriter:
	def __init__(self,io):
		self.io = io
	@property
	def fp(self):
		return self.io.fp
	
	def str(self,s,run=0):
		try:
			with open(self.fp,'w') as f:
				f.write(s)
			if run:
				self.io.run()
		except:
			perr()
			return None
	
	def ar(self,ar,sep='\n'):
		return self.str(sep.join(ar))
	
	def json(self,ob,indent=4,carefull=0,run=0):
		fp = self.fp
		
		def write(to_fp):
			with open(to_fp,'w') as f:
				json.dump(ob,f,indent=indent)
		
		if carefull:
			fp_tmp = self.io.dir + self.io.base + str(time()) + '.tmp'
			write(fp_tmp)
			if self.io.read.json(fp_tmp) is not None:
				shutil.move(fp_tmp,fp)
				return True
			else:
				JiviFile.delete(fp)
			
			return
		
		else:
			write(fp)
		if run:
			self.io.run()
		
	
class JiviIO:
	fp:str
	read:JiviIOReader
	write:JiviIOWriter
	def __init__(self,*a,**b):
		self.fp = JiviFile.fp(*a,**b)
		self.read  = JiviIOReader(self)
		self.write = JiviIOWriter(self)
	
	@property
	def base(self):
		return JiviFile.name(self.fp,ex=True)
	@property
	def baselower(self):
		return JiviFile.name(self.fp,ex=True,lower=True)
	@property
	def name(self):
		return JiviFile.name(self.fp,ex=False)
	@property
	def namelower(self):
		return JiviFile.name(self.fp,ex=False,lower=True)
	@property
	def ex(self):
		return JiviFile.ex(self.fp)
	@property
	def dir(self):
		return JiviFile.dir(self.fp)

	def run(self):
		os.system(f'mf "{self.fp}"')
class JiviStr:

	@classmethod
	def tabs(cls,s,length,sep='\t'):
		tabs        = math.ceil(length/4)
		tabs_string = math.floor(len(s)/4)
		s           = sep*max(0,tabs-tabs_string)
		return s
	
	@classmethod
	def tabbed(cls,s,length,sep='\t'):
		return s + cls.tabs(s,length,sep=sep)
	
		
	@classmethod
	def tab(cls,tab):
		keys    = list(tab.keys())
		max_len = len(max(keys,key=len))
		return "\n".join(["{k} : {v}".format(k=cls.tabbed(k,max_len),v=tab[k]) for k in keys])

	@classmethod
	def minlen(cls,s,i):
		return ''.join([str(s)," "*(i - len(str(s)))])


class JiviAr:
	@classmethod
	def split_by_stepsize(cls,ar:list,stepsize=5,as_gen=True) -> [list]:
		def func():
			for i in range(0, len(ar), stepsize):
				yield ar[i:i + stepsize]

		if not as_gen:
			return list(func())
		return func()
	@classmethod
	def split_into_parts(cls,ar:list,parts=5,as_gen=True) -> [list]:
		def func():
			c = math.ceil(len(ar)/parts)
			if c == 0: return
			for i in range(0, len(ar), c):
				yield ar[i:i + c]
		if not as_gen:
			return list(func())
		return func()

	@classmethod
	def join_start_too(cls,ar:list,sep:str) -> str:
		return sep + sep.join(ar) if len(ar) else ''

class JiVi:
	class ALL:
		JiviCore   = JiviCore
		JiviAr  = JiviAr
		JiviDir = JiviDir
		JiviFile   = JiviFile
		JiviIO  = JiviIO
		JiviStr   = JiviStr
	
	C   = JiviCore
	Ar  = JiviAr
	Dir = JiviDir
	F   = JiviFile
	IO  = JiviIO
	S   = JiviStr

def __test():
	test_ar = ['a1','a2','a3','b1','b2','b3','c1','c2','c3','d1','d2','d3']
	assert len(JiviAr.split_by_stepsize(test_ar,3,as_gen=False)[0]) == 3
	assert len(JiviAr.split_into_parts(test_ar,4,as_gen=False)) == 4
	
if __name__ == "__main__":
	__test()
		
	