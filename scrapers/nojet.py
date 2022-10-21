#!/usr/bin/env python
# -*- encoding: utf-8 -*-

URL = "https://eurest.mashie.com/public/menu/restaurang+n%C3%B6jet/60f56fd6?country=se"

def get_daily_specials(day=None):
	from bs4 import BeautifulSoup
	import urllib.request
	import ssl

	daily_specials = {
		"name": "Restaurang Nöjet",
		"specials": [],
		"streetaddress": "Sundsvalls Sjukhus, Lasarettsvägen",
		"dataurl": URL,
		"mapurl": "http://www.hitta.se/sundsvalls+sjukhus/sundsvall/LzggZC-vvm?vad=sundsvalls+sjukhus"
	}

	ctx = ssl.create_default_context()
	ctx.check_hostname = False
	ctx.verify_mode = ssl.CERT_NONE

	page = urllib.request.urlopen(URL, context=ctx)
	soup = BeautifulSoup(page)
	page.close()

	div = soup.find("div", {"class": "row day-current"})
	if div != None:
		for t in  div.findNextSiblings():
			daily_specials["specials"].append(t.find("section", {"class": "day-alternative"}).find("span").text)

	return daily_specials

def main():
	import test
	test.run(get_daily_specials)

if __name__ == "__main__":
	main()

