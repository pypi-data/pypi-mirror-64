from urllib.request import urlopen,Request

		
def html(url):

	def getBody(txt):
		body = txt
		try:
			tl = txt.lower()
			a = tl.find('<body')
			b = tl.find('>',a+1)
			c = tl.find('</body>',b)
			body = txt[b+1:c]
		except:
			pass
		
		
		return body
	user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'
	headers = { 'User-Agent' : user_agent }
	req = Request(url, None, headers)
	resp = urlopen(req)

	html = resp.read()
	try:
		txt = html.decode()
		return getBody(txt)
	except:
		return html
