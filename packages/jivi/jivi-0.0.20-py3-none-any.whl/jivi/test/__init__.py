from __future__ 		import annotations


def get_all():
	from .download 			import DownloadTester
	from .fs				import FSTester
	from .menu				import MenuTester
	from .util				import UtilTester
	from .wrapper			import WrapperTester
	from .menu_plugin   	import PluginTester

	return {k : v for k,v in locals().items()}






class Test:
	def __init__(self):
		from .tester import Tester
		from ..util  import Pause,Clearterminal
		current_tester : Tester = None
		from ..menu.menu 	import Ctrl
		from ..menu.plugin 	import YesNoQuestion
		ctrl = Ctrl()
		def cb(val):
			if val:
				ctrl.exit()
				current_tester.do()
				Pause()
			else:
				pass
			ctrl.stop()
	

		for k,v in get_all().items():
			current_tester = v
			YesNoQuestion(f"Test {k} ?",ctrl,cb=cb)
			ctrl.display()
		ctrl.exit()
	@classmethod
	def optionMenu(cls):
		from .tester import Tester
		from ..util  import Pause,Clearterminal
		current_tester : Tester = None
		from ..menu.menu 	import Ctrl,MenuItem
		ctrl = Ctrl()

		@ctrl.on_key('esc')
		def f(*a,**b):
			ctrl.exit()
			
		mainMenu = ctrl.create_menu("Select item to test")

		for k,v in get_all().items():
			@mainMenu.item(k,data=v)
			def on_click(mi:MenuItem):
				ctrl.cur.stop()
				mi.data.do()
				Pause()
		ctrl.display()

		ctrl.stop()
		ctrl.exit()
