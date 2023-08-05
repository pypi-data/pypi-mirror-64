from . import JDir,JFile

from .. import util

fp_test_dir = "C:\\temp\\testdir"


class FSTester(util.Tester):
	def files(self):
		def create_remove():
			d = JFile(fp_test_dir,"testfile.txt")
			d.delete()
			if d.exists:
				return "delete"
				
			d.writer.text("test")
			if not d.exists:
				return "write create"

			txt = d.reader.text()
			if txt is None:
				return "reader"

			if txt != "test":
				return "reader wrong text"
		

		def json():
			d = JFile(fp_test_dir,"testfile.json")
			test_ob = dict(a=1,b=4)
			if not d.writer.json(test_ob,carefull=True):
				return "json"

			d.delete()
			if d.exists:
				return "delete"
		return [create_remove,json]

	
	def dirs(self):
		import os


		def create_remove():
			d = JDir(fp_test_dir)
			
			d.delete_full()
			if d.exists:
				return "delete"
				
			JDir(fp_test_dir).create()
			if not d.exists:
				return "create"
		
		return [create_remove]
	
		







