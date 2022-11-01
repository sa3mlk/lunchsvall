#!/usr/bin/env python
# -*- encoding: utf8 -*-

from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import date

URL = "https://www.elite.se/sv/hotell/sundsvall/hotel-knaust/lunchmeny/"

def get_daily_specials(day=None):
	page = urlopen(URL)
	soup = BeautifulSoup(page)
	page.close()

	daily_specials = {
		"name": "Elite Hotel Knaust",
		"specials": [],
		"streetaddress": "Storgatan 13, Sundsvall",
		"dataurl": URL,
		"mapurl": ""
	}

	if day == None:
		day = date.today().weekday()

	# No lunch on Saturday or Sunday
	if day == 5 or day == 6:
		return daily_specials

	day = [u"Måndag", u"Tisdag", u"Onsdag", u"Torsdag", u"Fredag"][day]
	div = soup.find("div", {"class": "hidden-xs"}).find("strong", text=day)
	daily_specials["specials"].extend(div.findAllNext(text=True, limit=3))

	return daily_specials

def main():
	import test
	test.run(get_daily_specials)

if __name__ == "__main__":
	main()

