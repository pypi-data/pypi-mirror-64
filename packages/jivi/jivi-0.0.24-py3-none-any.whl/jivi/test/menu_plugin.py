from .tester import Tester
from ..menu.plugin import *

class PluginTester(Tester):
	def test(self):
		def get_cb(name):
			def cb(*a,**b):
				print(name,*a,**b)

			return cb

		def explorer():
			e = Explorer("Explorer test",cb=get_cb("explor"))
			e.display()
		def selecter():
			s = Selecter("Selecter test",SelecterOption("option a",1),SelecterOption("option b",2),cb=get_cb("se"))
		def yon():
			i = YesNoQuestion("Werkt dit ?",cb=get_cb("yon"))
		def textinput():
			i = TextInput("TextInput test",cb=get_cb("text input"))

		return [explorer,selecter,yon,textinput]