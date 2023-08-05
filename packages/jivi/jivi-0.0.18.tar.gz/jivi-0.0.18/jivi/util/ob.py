

def properties_keys_tab(ob):
	return {k : True for k in ob.__dict__.keys()}

def properties_keys_ar(ob):
	return list(ob.__dict__.keys())

