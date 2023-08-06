from . import Validator


class InputParameter(IHasReplacement_tab):
	def __init__(self,
		name        : str,            
		validators  : List[Validator.Validator]=[],
		desc        : str              = None,
		ex          : List[str]        = [],
		start_dir   : str              = None,
		max_size    : int              = None,
		min_size    : int              = None,
		min_len     : int              = None,
		max_len     : int              = None
	):
		self.name       = name
		self.validators = validators
		self.desc       = desc
		self.ex         = ex
		self.start_dir  = start_dir
		self.max_size   = max_size
		self.min_size   = min_size
		self.max_len    = max_len
		self.min_len    = min_len

	@property
	def replacement_tab(self):
		return dict(
		name       = self.name,
		desc       = self.desc)