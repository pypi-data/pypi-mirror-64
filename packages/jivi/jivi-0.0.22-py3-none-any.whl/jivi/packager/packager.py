from ..util 		import download,string
from ..fs 			import JDir,JFile
from ..wrapper 		import jvWrapper,jvWrapperSuper
from typing 		import List
from ..jv 			import jv



DEBUG = False


class CONSTANT:
	packagename     : str  
	version         : str  
	fConfigFile     : JFile
	fSetupFile      : JFile
	dPythonPackages : JDir 
	dPythonPackage  : JDir 
	dPackage        : JDir 
	dSettings       : JDir 
	dMainDir        : JDir 
	dDist			: JDir

	fBatBuild		: JFile
	fBatUpload	    : JFile



@jvWrapper()
class CONSTANT_SETTER(jvWrapperSuper):
	current_function_name : str
	def __init__(self):
		pass

	def init(self):
		def add():
			def decorater(f):
				self.current_function_name = f.__name__
				if not f():
					self.error('miauw')
			return decorater
		
		def must_exist(d):
			return d and d.exists
		
		def try_setting(*conditions,key=None,value=None):
			pass
		
		
		@add()
		def dMainDir():
			CONSTANT.dMainDir = JFile(__file__).parent_dir_ob
			return CONSTANT.dMainDir.exists
		@add()
		def dSettings():
			CONSTANT.dSettings = CONSTANT.dMainDir.copyob.down('settings')
			return CONSTANT.dSettings.exists
		
		@add()
		def fConfigFile():
			CONSTANT.fConfigFile = CONSTANT.dSettings.file("config.json")
			return CONSTANT.fConfigFile.exists
		
		@add()
		def fSetupFile():
			CONSTANT.fSetupFile = CONSTANT.dSettings.file("setup.py")
			return CONSTANT.fSetupFile.exists
		
		@add()
		def version():
			CONSTANT.version = CONSTANT.fConfigFile.reader.json().get('version')
			return True
		
		@add()
		def packagename():
			CONSTANT.packagename = CONSTANT.fConfigFile.reader.json().get('packagename')
			return True
		
		@add()
		def dPythonPackage():
			CONSTANT.dPythonPackage = JFile(jv.__file__).parent_dir_ob
			return CONSTANT.dPythonPackage.exists
		
		@add()
		def dPythonPackages():
			CONSTANT.dPythonPackages = CONSTANT.dPythonPackage.parent_dir_ob
			return CONSTANT.dPythonPackages.exists
		
		@add()
		def dPackage():
			CONSTANT.dPackage = CONSTANT.dMainDir.copyob.down('data','current')
			return True
		
		@add()
		def dDist():
			CONSTANT.dDist = CONSTANT.dPackage.copyob.down('dist')
			return True	
		
		@add()
		def bats():
			dBat = CONSTANT.dSettings.copyob.down('bats')
			CONSTANT.fBatBuild = dBat.file('build.bat')
			CONSTANT.fBatUpload = dBat.file('upload.bat')
			return CONSTANT.fBatBuild.exists and CONSTANT.fBatUpload.exists
	
	def error(self,*a):
		self.jvlog.critical(self.current_function_name,*a)
		exit()
	
	def set_next_version_from_site(self):
		url = f"https://pypi.org/project/{CONSTANT.packagename}/"

		def get_html():
			if DEBUG:
				return CONSTANT.dSettings.file("test.html").reader.text(encoding="utf8")
			return download.html(url)

		html = get_html()
		if not html:
			return self.error("set_next_version_from_site", "failed to download",url)
			
		version = string.between(html,'package-header__name">','</h1>')
		if not version:
			return self.error("set_next_version_from_site", "failed to read between",html)

		version = version.replace(CONSTANT.packagename,'').strip()

		old_version = CONSTANT.version
		CONSTANT.version = "0.0.{i}".format(i=int(version.split('.')[-1]) + 1)


		keys = list(CONSTANT.fConfigFile.reader.json().keys())
		self.jvlog.info(f"Version {old_version} -> {CONSTANT.version}")

		CONSTANT.fConfigFile.writer.json({k : getattr(CONSTANT,k) for k in keys})
		

	@classmethod
	def do(cls):
		c = cls()
		c.init()
		c.set_next_version_from_site()

CONSTANT_SETTER.do()



@jvWrapper()
class PackageUploader(jvWrapperSuper):

	current_function_name : str
	def __init__(self):
		pass
	
	def error(self,*a):
		self.jvlog.critical(self.current_function_name,*a)
		exit()


	def init(self):
		def add():
			def decorater(f):
				self.current_function_name = f.__name__
				if not f():
					self.error('miauw')
			return decorater
		

		@add()
		def del_dPackage():
			return CONSTANT.dPackage.delete_full()
		@add()
		def create_dPackage():
			return CONSTANT.dPackage.create()
		@add()
		def create_dPackageDirs():
			for d in list(filter(lambda x : x.lname != "__pycache__",CONSTANT.dPythonPackage.reader.dirs_ob(deep=True))):
				d_to = CONSTANT.dPackage.copyob.down(d.rel(CONSTANT.dPythonPackages))
				if not d_to.create():
					return False
			return True
		@add()
		def copy_dPackageFiles():
			def file_filter(f:JFile):
				if f.fp.lower().find('__pycache__') != -1:
					return False
				if f.lex == 'cfg':
					return False
				return True
			
			for f_from in list(filter(file_filter,CONSTANT.dPythonPackage.reader.files_ob(deep=True))):
				f_parent_dir = f_from.parent_dir_ob
				d_to_parent_dir = CONSTANT.dPackage.copyob.down(f_parent_dir.rel(CONSTANT.dPythonPackages))
				f_to = f_from.copyob
				f_to.parent_dir_fp = d_to_parent_dir.fp
				if not f_from.copy(f_to.fp,True):
					return False
			return True
		@add()
		def copy_build_files():
			to_file = CONSTANT.fSetupFile.copyob
			to_file.parent_dir_fp = CONSTANT.dPackage.fp
			return CONSTANT.fSetupFile.copy(to_file.fp,True)


		@add()
		def del_dist():
			return CONSTANT.dDist.delete_full()
		
		bat_start_options = dict(wait=True,same_window=True,start_dir=CONSTANT.dPackage.fp)
		bat_start_options = dict(wait=True,same_window=False,start_dir=CONSTANT.dPackage.fp)


		@add()
		def create_build():

			CONSTANT.fBatBuild.start(title=f"{CONSTANT.packagename} builder",**bat_start_options)
			return True
		
		@add()
		def upload():
			CONSTANT.fBatUpload.start(title=f"{CONSTANT.packagename} uploader",**bat_start_options)
			return True



pu = PackageUploader()

pu.init()
