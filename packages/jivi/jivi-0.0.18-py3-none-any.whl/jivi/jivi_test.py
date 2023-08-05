from .downloader.download_test import DownloadTester
from .fs.fs_test import FSTester
from .menu.menu_test import MenuTester
from .util.util_test import UtilTester
from .wrapper.wrapper_test import WrapperTester



class JiviTester:
	download = DownloadTester
	fs = FSTester
	menu = MenuTester
	util = UtilTester
	wrapper = WrapperTester

	@classmethod
	def reset(cls):
		cls.download = DownloadTester
		cls.fs = FSTester
		cls.menu = MenuTester
		cls.util = UtilTester
		cls.wrapper = WrapperTester



	@classmethod
	def only(cls,*names):
		ar = []
		for n in names:
			if isinstance(n,str):
				ar.append(getattr(cls,n,None))
			else:
				ar.append(n)

		return cls.do(ar)

	@classmethod
	def do(cls,ar=None):
		if ar is None:
			ar = [cls.download,cls.fs,cls.menu,cls.util,cls.wrapper]
		for x in ar:
			if not x:
				continue
			x.do()
