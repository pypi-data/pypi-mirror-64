import random as _random



def fill_to_len(s:str,min_len:int,filler=' ',left_side=True):
	if len(s) >= min_len:
		return s
	if left_side:
		return filler*(min_len - len(s)) + s
	
	return s + filler*(min_len - len(s))

def between(s:str,a:str,b:str) -> str:
	try:
		x = s.find(a)
		y = s.find(b,x+len(a))
		retval = s[x+len(a):y]
		return retval
	except:
		return None


def random(n=10):
	letters = 'abcdefghijklmnopqrstuvwxyz0123456789'
	return ''.join(_random.choice(letters) for i in range(n))


def same_len_ar(ar,to_string=True):
	max_lens = []
	for i,a in enumerate(ar):
		if not i:
			max_lens = [len(a_el) for a_el in a]
		else:
			max_lens = [max(max_lens[a_ind],len(a[a_ind])) for a_ind in range(len(a))]
	
	ret_val = []
	for x in ar:
		ret_val.append(' '.join([fill_to_len(s,min_len=max_lens[index],left_side=False) for index,s in enumerate(x)]))
	

	return ret_val
