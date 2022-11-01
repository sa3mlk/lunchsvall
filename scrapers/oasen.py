#!/usr/bin/env python
# -*- encoding: utf-8 -*-

URL = "https://eurest.mashie.com/public/menu/restaurang+%c3%a5kroken/oasen?country=se"

def get_daily_specials(day=None):
	from bs4 import BeautifulSoup
	import urllib.request
	import ssl

	daily_specials = {
		"name": "Restaurang Oasen",
		"specials": [],
		"streetaddress": "Södra Järnvägsgatan 41, Sundsvall",
		"dataurl": URL,
		"mapurl": "https://www.hitta.se/v%C3%A4sternorrlands+l%C3%A4n/sundsvall/s%C3%B6dra+j%C3%A4rnv%C3%A4gsgatan+41/omr%C3%A5de/62.387966479770704:17.296699352772933"
	}

	ctx = ssl.create_default_context()
	ctx.check_hostname = False
	ctx.verify_mode = ssl.CERT_NONE

	page = urllib.request.urlopen(URL, context=ctx)
	soup = BeautifulSoup(page)
	page.close()

	div = soup.find("div", {"class": "row day-current "})
	if div != None:
		for t in  div.findNextSiblings():
			daily_specials["specials"].append(t.find("section", {"class": "day-alternative"}).find("span").text)

	return daily_specials

def main():
	import test
	test.run(get_daily_specials)

if __name__ == "__main__":
	main()

