from ..downloader 		import Download
import os 
from time 		import sleep
from _thread 	import start_new_thread as Thread
from ..fs 		import JFile
from .tester	import Tester
from ..			import util
URL = '''
http://praktijkdelotus.be/3.rar
'''.strip()

jFile = JFile(r'C:\temp\3.rar')
jFile.delete()

class DownloadTest(Download):
	def test(self):
		def data_test():
			to_print_ar = []
			prop_names = 'total,downloaded,written,to_download,to_write,speed'.split(',')
			for n in prop_names:
				to_print_ar.append([n,' : ',getattr(self.dataHuman,n)])
			for x in util.String.same_len_ar(to_print_ar):
				print(x)
			print('--------')

		def control_test():
			prop_names = 'start,stop,reset,move'.split(',')
			prop_names = 'stop,reset,move'.split(',')
			for n in prop_names:
				print(f'{n} : {getattr(self.control,n)()}')
			print('--------')

		data_test()
	
class DownloadTester(Tester):
	def test(self):
		def download_test_normal():
			downloader = DownloadTest(URL,jFile.fp)
			def printer():
				while True:
					if downloader.status.finished:
						break
					downloader.test()
					sleep(5)


				print("test finished")
				exit()
			downloader.control.start()
			Thread(printer,())
			while not downloader.status.finished:
				sleep(1)
		return [download_test_normal]
