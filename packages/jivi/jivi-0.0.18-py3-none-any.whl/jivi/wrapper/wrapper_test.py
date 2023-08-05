from jivi import jvWrapper,jvWrapperSuper
from .. import util

@jvWrapper()
class Order(jvWrapperSuper):
	
	def __init__(self,id:int,klant:str,bedrag:int):
		self.id = id
		self.klant = klant
		self.bedrag = bedrag

		self.jvlog.info('test')


	def test(self):
		self.jvlog.warning('warning ooh')


class WrapperTester(util.Tester):
	def test(self):
		def wrapper_test():

			order = Order(1,'test klant',5000)
			order.test()

			print(order)

		return [wrapper_test]