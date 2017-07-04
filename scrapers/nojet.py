#!/usr/bin/env python
# -*- encoding: utf-8 -*-

URL = "http://eurest.mashie.eu/public/menu/restaurang+n%C3%B6jet/60f56fd6"

def get_daily_specials(day=None):
	from BeautifulSoup import BeautifulSoup
	from urllib2 import urlopen

	daily_specials = {
		"name": "Restaurang Nöjet",
		"specials": [],
		"streetaddress": "Sundsvalls Sjukhus, Lasarettsvägen",
		"dataurl": URL,
		"mapurl": "http://www.hitta.se/sundsvalls+sjukhus/sundsvall/LzggZC-vvm?vad=sundsvalls+sjukhus"
	}

	page = urlopen(URL)
	soup = BeautifulSoup(page)
	page.close()

	div = soup.find("div", {"class": "row day-current "})
	for t in  div.findNextSiblings():
		daily_specials["specials"].append(t.find("section", {"class": "day-alternative"}).find("span").text)

	return daily_specials

def main():
	import test
	test.run(get_daily_specials)

if __name__ == "__main__":
	main()

