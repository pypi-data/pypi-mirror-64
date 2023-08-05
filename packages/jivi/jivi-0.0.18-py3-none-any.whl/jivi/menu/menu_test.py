from jivi import jv


class MenuTester(jv.util.Tester):
	def Menu(self):
		def test():
			menu = jv.menu.Menu(max_rows_auto=True)

			def maak_aantal_startend_met(aantal:int,startend:str):
				for i in range(aantal):
					naam = startend + jv.util.string.random(10)
					@menu.item(naam,exit_after=True)
					def print_test(p:jv.menu.Param):
						print(p.itemClicked)
						return True


			maak_aantal_startend_met(20,'jor ')
			maak_aantal_startend_met(20,'lot ')
			maak_aantal_startend_met(20,'jon ')
			maak_aantal_startend_met(20,'aka ')
			maak_aantal_startend_met(20,'deepthroat ')

			menu.display()

		return [test]

