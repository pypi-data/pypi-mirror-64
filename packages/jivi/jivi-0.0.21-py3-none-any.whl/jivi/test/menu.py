from ..menu import Menu,MenuItem,Ctrl,addon
from .tester import Tester


class MenuTester(Tester):
	def test(self):
		def test_one():
			menuCtrl = Ctrl(max_lines=29)
			print(menuCtrl.cur.color.normal)
			addon.Searcher(menuCtrl)
			addon.FirstLetter(menuCtrl)
			addon.Scrollbar(menuCtrl)
			addon.Searchbox(menuCtrl)
			mainMain = menuCtrl.create_menu("Test")
			names = ["Joris","Lotte","Kevin","Davy","Ronny","Anke","Aars","Jan","Loes","Lies","Lore"]


			for i in range(2000):
				@mainMain.item(f"testing {i}",data=i)
				def on_click(mi:MenuItem):
					print(mi.data)
					mi.ctrl.stop()

			for n in names:
				@mainMain.item(n,data=n)
				def test_func(mi:MenuItem):
					print(f"OK {mi.data}")
					mi.ctrl.stop()
			menuCtrl.display()

		return [test_one]



