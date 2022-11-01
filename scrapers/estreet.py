#!/usr/bin/env python
# -*- encoding: utf-8 -*-

URL = "http://www.estreet.nu"

def get_daily_specials(day=None):
	from bs4 import BeautifulSoup
	from urllib.request import urlopen
	from datetime import date

	day = date.today().weekday() if day is None else day

	daily_specials = {
		"name": "E-street",
		"specials": [],
		"streetaddress": "Esplanaden 14, Sundsvall",
		"dataurl": URL,
		"mapurl": "http://www.hitta.se/e+street/sundsvall/zzzRPjw5X4?vad=e-street&var=sundsvall"
	}

	try:
		day = [u"Måndag", u"Tisdag", u"Onsdag", u"Torsdag", u"Fredag"][day]
	except IndexError:
		return daily_specials

	page = urlopen(URL)
	soup = BeautifulSoup(page)
	page.close()

	div = soup.find("div", id="gg_lunch_widget-3")
	day_title = div.find(lambda tag: tag.name == "h6" and tag.text == day)
	daily_specials["specials"] = filter(len, day_title.findNext("p").text.split("-"))

	return daily_specials

def main():
	import test
	test.run(get_daily_specials)

if __name__ == "__main__":
	main()
