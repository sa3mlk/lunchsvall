#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from BeautifulSoup import BeautifulSoup, Tag
from urllib2 import urlopen
from datetime import date
import re

URL = "https://www.max.se/sv/Maten/Meny/Maltider/Dagens-Lunch/"

def get_daily_specials(day = None):
	page = urlopen(URL)
	soup = BeautifulSoup(page)
	page.close()

	daily_specials = {
		"name": "mAx",
		"specials": [],
		"streetaddress": "Landsvägsallén 5, Sundsvall",
		"dataurl": URL,
		"mapurl": "http://www.hitta.se/ViewDetailsPink.aspx?Vkiid=mFQRqbiq0V2C0M4wvtGY0w%253d%253d"
	}

	day = date.today().weekday() if day is None else day

	# Only Monday - Friday
	if day > 4:
		return daily_specials

	span = filter(lambda t: type(t) is Tag, soup.find("ul", {"class": "price"}).contents)[day].span.text
	split = span.find(" - ")
	if split == -1:
		split = span.find("&nbsp;")
		split += 6 if split > 0 else 0
	else:
		split += 3
	split = 0 if split is -1 else split
	daily_specials["specials"].append(span[split:].strip())

	return daily_specials

def main():
	for d in range(5):
		data = get_daily_specials(d)
		print "Day {d}".format(d=d)
		for c in data["specials"]:
			print "  ", c

if __name__ == "__main__":
	main()

