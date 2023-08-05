import math
from datetime import datetime
import subprocess

def Popen(s):
	try:
		process = subprocess.Popen(s, stdout=subprocess.PIPE,shell=1)
		stdout, stderr = process.communicate()
		if stderr: print(stderr)
		
		stdout = stdout.decode("cp850")
		for x in stdout.splitlines():
			yield x.strip()
	except:
		pass
	
class to_string:
	__BYTE_HELPER = [[math.pow(1024,i),name] for i,name in enumerate(["bytes","KB","MB","GB","TB"])]
	__BYTE_HELPER.reverse()
	@classmethod
	def bytes(cls,number_of_bytes):
		number_of_bytes = float(number_of_bytes)
		if not number_of_bytes:
			return "0 bytes"
		for a in cls.__BYTE_HELPER:
			n = number_of_bytes/a[0]
			if n >= 1:
				return "{a} {b}".format(a=round(n,2),b=a[1])
	@classmethod
	def sec(cls,s):
		h = math.floor(s/3600)
		s -= h*3600
		m =  math.floor(s/60)
		s -= m*60
		return "%02d:%02d:%02d" % (h,m,s)

	@classmethod
	def unix(cls,i):
		return datetime.utcfromtimestamp(i).strftime('%Y-%m-%d %H:%M:%S')


def to_int(n):
	try:
		retval = int(n)
		return retval
	except:
		return None

		