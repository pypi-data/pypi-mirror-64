from .tester import Tester
from ..uinput import UIInput,Validator,ValueGetter,InputParameter


class UIInputTester(Tester):
	def test(self):
		def create_and_print():
			x = UIInput.String(para=InputParameter(name="Email",validators=[Validator.StringNotEmpty,Validator.Email]))
			for inputMethod in x.inputMethods:
				print(inputMethod)

		return [create_and_print]

	