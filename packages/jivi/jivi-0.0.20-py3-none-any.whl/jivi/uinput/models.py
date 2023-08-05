from ..util.ob import copy_tab
from typing import List
def string_replacer(s,tab,**t):
	for k,v in tab.items():
		if v is None:
			continue
		s = s.replace(f'[{k}]',v)
	return s

class IHasReplacement_tab:
	@property
	def replacement_tab(self):
		return dict()


