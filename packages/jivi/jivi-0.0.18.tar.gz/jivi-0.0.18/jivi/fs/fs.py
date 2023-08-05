from __future__ import annotations
import os,json,shutil
from time import time
from typing import List

def inttime():
	return int(time())

get_rel = os.path.relpath

def get_ex_from_fp(fp,lower=False):
	retval =  os.path.splitext(fp)[1][1:]
	return retval.lower() if lower else retval

class JDirChildWrapper:
	def __init__(self,parent:JDirFileWrapper):
		self.parent = parent
	
	@property
	def fp(self):
		return self.parent.fp



class JDirFileWrapper:
	isfile : bool = False
	isdir : bool = False
	__fp : str
	def __init__(self,*parts):
		self.set_fp(*parts)
	
	def set_fp(self,*value):
		self.__fp = os.path.abspath(os.path.join(*value))

	@property
	def all_parent_dir_ob(self):
		p = self.parent_dir_ob
		old_fp = ''
		retval = [] 
		while p.fp != old_fp:
			old_fp = p.fp
			retval.append(p.copyob)
			p = p.copyob.up(1)
		
		return retval
	
	@property
	def parent_dir_ob(self):
		return JDir(self.parent_dir_fp)
	
	@property
	def parent_dir_fp(self):
		if self.isdir:
			return os.path.dirname(os.path.abspath(os.path.join(self.fp,'..')))
		if self.isfile:
			return os.path.dirname(self.fp)
		
		print("HOW SHIT")
		print(self.fp)
		exit()
	
	@parent_dir_fp.setter
	def parent_dir_fp(self,value):
		self.set_fp(value,self.name)

	@property
	def fp(self):
		return self.__fp
	
	@fp.setter
	def fp(self,*value):
		self.set_fp(*value)
	
	@property
	def name(self):
		return os.path.basename(self.fp)
	
	@name.setter
	def name(self,value):
		self.set_fp(self.parent_dir_fp,value)

	@property
	def lname(self):
		return self.name.lower()
	
	@property
	def modified(self):
		return os.path.getmtime(self.fp)
	
	@property
	def created(self):
		return os.path.getctime(self.fp)

	@property
	def copyob(self):
		if self.isdir:
			return JDir(self.fp)
		if self.isfile:
			return JFile(self.fp)
		
		print("copy HOW SHIT")
		print(self.fp)
		exit()

class JFileReader(JDirChildWrapper):
	def json(self,encoding=None,mode='r'):
		try:
			with open(self.fp,mode,encoding=encoding) as f:
				a = json.load(f)
				return a
		except:
			return None
	def text(self,encoding=None,mode='r'):
		try:
			with open(self.fp,mode,encoding=encoding) as f:
				txt = f.read()
				return txt
		except:
			return None
	def lines(self,encoding=None,mode='r',strip=True):

		txt = self.text(encoding=encoding,mode=mode)
		if txt is None:
			return txt
		for x in txt.splitlines():
			if not strip:
				return x
			x = x.strip()
			if x:
				return x
		
class JFileWriter(JDirChildWrapper):
	
	def text(self,txt,mode='w',encoding=None):
		with open(self.fp,mode,encoding=encoding) as f:
			f.write(txt)

	def lines(self,*lines,seperator="\n",mode='w',encoding=None):
		self.text(seperator.join(map(str,lines)))
	
	def json(self,ob,indent=4,carefull=False,debug=False):
		if carefull:
			tmp_file : JFile = self.parent.copyob
			
			tmp_file.name = f"{inttime()}{self.parent.name_without_ex}.tmp"

			if not tmp_file.writer.json(ob,indent=indent,carefull=False):
				if debug:
					print(f"Failed to write {tmp_file}")

				return False
			
			if tmp_file.reader.json() is None:
				if debug:
					print(f"Failed read {tmp_file}")
			else:
				if tmp_file.move(self.fp):
					return True
				else:
					print("Something went wrong")
					exit()
			
			tmp_file.delete()
			return False
			
		else:
			try:

				with open(self.fp,'w') as f:
					json.dump(ob,f,indent=indent)

				return True

			except:
				return False
		
	


class JDirReader(JDirChildWrapper):
	def get(self,asob=True,deep=True,dirs=True,files=True,ex=[],rel=False):
		dirs_todo = [self.fp]
		self_fp = self.fp[:]
		ex_tab = {k.lower() : True for k in ([ex] if isinstance(ex,str) else ex)}
		ex_check = True if ex_tab else False
		rel_path = ''

		while dirs_todo:
			new_dirs_todo = []
			for fp_dir in dirs_todo:
				if rel:
					rel_path = get_rel(fp_dir,self_fp)
					if rel_path == '.':
						rel_path = ''
					else:
						rel_path = rel_path + os.sep
					
				for x in os.listdir(fp_dir):
					fp = fp_dir + os.sep + x
					if os.path.isfile(fp):
						if not files:
							continue
						if ex_check and (not get_ex_from_fp(fp,True) in ex_tab):
							continue
						yield JFile(fp) if asob else (rel_path + x if rel else fp)
						
					else:
						if deep:
							new_dirs_todo.append(fp)
						if not dirs:
							continue
						yield JDir(fp) if asob else (rel_path + x if rel else fp)
			dirs_todo = new_dirs_todo
		
	def files(self,asob=True,deep=True,ex=[],rel=False):
		return self.get(asob=asob,deep=deep,ex=ex,rel=rel,files=True,dirs=False)
	
	def files_ob(self,deep=True,ex=[]) -> List[JFile]:
		return self.get(asob=True,deep=deep,ex=ex,rel=False,files=True,dirs=False)

	def dirs(self,asob=True,deep=True,rel=False):
		return self.get(asob=asob,deep=deep,rel=rel,files=False,dirs=True)

	def dirs_ob(self,deep=True) -> List[JDir]:
		return self.get(asob=True,deep=deep,rel=False,files=False,dirs=True)




class JFile(JDirFileWrapper):
	isfile = True
	isdir = False
	reader : JFileReader
	writer : JFileWriter
	def __init__(self,*parts):
		super().__init__(*parts)
		self.reader = JFileReader(self)
		self.writer = JFileWriter(self)

	def copy(self,fp_to,carefull=False):
		try:
			shutil.copy(self.fp,fp_to)
			retval = JFile(fp_to)
			if carefull and not retval.exists:
				return None
			return retval
		except:
			return None

	def move(self,fp_to):
		try:
			shutil.move(self.fp,fp_to)
			self.fp = fp_to
			return True
		except:
			return False
		
	def start(self,same_window=False,start_dir=None,title=None,wait=False,minimized=False,maximized=False):
		attr = []
		if start_dir:
			attr.append(f'/D "{start_dir}"')
		if minimized:
			attr.append("/MIN")
		if maximized:
			attr.append("/MAX")
		if wait:
			attr.append("/WAIT")
		if same_window:
			attr.append("/B")
		
		attr = ' '.join(attr)
		title = self.name_without_ex if title is None else title
		cmd = f'start {attr} "{self.name_without_ex}" "{self.fp}"'
		print(cmd)
		os.system(cmd)
	
	def delete(self):
		try:
			os.remove(self.fp)
			return True
		except:
			return False
		

	@property
	def exists(self):
		return os.path.isfile(self.fp)

	def __repr__(self):
		return f'[JFile] {self.fp}'
	
	@property
	def ex(self):
		return os.path.splitext(self.fp)[1][1:]
	
	@ex.setter
	def ex(self,value):
		self.name = self.name_without_ex + '.' + value
	

	@property
	def name_without_ex(self):
		return os.path.splitext(os.path.basename(self.fp))[0]
	
	@property
	def lname_without_ex(self):
		return self.name_without_ex.lower()
	
	@property
	def lex(self):
		return self.ex.lower()
	
	@property
	def size(self):
		return os.path.getsize(self.fp)
	
class JDir(JDirFileWrapper):
	isfile = False
	isdir = True
	reader : JDirReader
	def __init__(self,*parts):
		super().__init__(*parts)
		self.reader = JDirReader(self)


	def isEmpty(self):
		for x in os.listdir(self.fp):
			return False
		return True


	@classmethod
	def cwd(cls):
		return cls(os.getcwd())
	

	def file(self,*parts) -> JFile:
		return JFile(self.fp,*parts)
	
	def up(self,n=1):
		self.set_fp(self.fp,*['..']*n)
		return self
	
	def down(self,*parts):
		self.set_fp(self.fp,*parts)
		return self

	def rel(self,fpOrDir):
		fp = fpOrDir.fp if isinstance(fpOrDir,JDir) else fpOrDir
		return os.path.relpath(self.fp,fp)

	def __repr__(self):
		return f'[JDir] {self.fp}'

	@property
	def exists(self):
		return os.path.isdir(self.fp)
	
	def create(self):
		if not self.exists:
			os.makedirs(self.fp)
		return self.exists

	
	def delete_full(self):
		try:
			if self.exists:
				shutil.rmtree(self.fp)

			return not self.exists
		except:
			return None

	def delete(self):
		try:
			os.rmdir(self.fp)
			return True
		except:
			return False

