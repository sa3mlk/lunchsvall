#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from bs4 import BeautifulSoup, NavigableString
from urllib.request import urlopen
from datetime import date

URL = "http://sundsvall.invitobar.se/mat/#section-invito-dryck"

def get_daily_specials(day=None):
	page = urlopen(URL)
	soup = BeautifulSoup(page)
	page.close()

	daily_specials = {
		"name": "Invito",
		"specials": [],
		"streetaddress": "Storgatan 6-8, Sundsvall",
		"dataurl": URL,
		"mapurl": "http://www.hitta.se/ViewDetailsPink.aspx?Vkiid=h7sTX8JwG1d8a10%252fW3RuwA%253d%253d&Vkid=2688685"
	}

	day = date.today().weekday() if day is None else day

	# Only Monday - Friday
	if day > 4:
		return daily_specials

	day = [u"Måndag", u"Tisdag", u"Onsdag", u"Torsdag", u"Fredag"][day]
	anchor = soup.find("div", {"id": "meny-objekt-veckans-lunch"})
	d = anchor.find("p", text=day).findParent("li")
	daily_specials["specials"] = list(filter(lambda x: len(x) > 6, [t.text for t in d.findAll("p")[1:]]))

	return daily_specials

def main():
	import test
	test.run(get_daily_specials)

if __name__ == "__main__":
	main()

