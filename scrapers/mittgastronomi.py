#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from BeautifulSoup import BeautifulSoup, NavigableString, Tag
from urllib2 import urlopen
from datetime import date
import re

URL = "http://www.mittgastronomi.com/menyer/dagenslunch"

def get_daily_specials(day=None):
	page = urlopen(URL)
	soup = BeautifulSoup(page)
	page.close()

	daily_specials = {
		"name": "Mitt Gastronomi",
		"specials": [],
		"streetaddress": "Russvägen 20, Sundsvall",
		"dataurl": URL,
		"mapurl": "http://www.hitta.se/ViewDetailsPink.aspx?Vkiid=WQ2HuqDz9prdTLqQwJejvg%253d%253d"
	}

	if day == None:
		day = date.today().weekday()

	# Only Monday - Friday
	if day > 4:
		return daily_specials

	day = [u"Måndag", u"Tisdag", u"Onsdag", u"Torsdag", u"Fredag"][day]
	anchor = soup.find("h3", text=day).parent

	specials = anchor.findNextSibling("p").text
	daily_specials["specials"] = filter(len, re.split("\d. ", specials))

	return daily_specials

def main():
	def print_specials(day, d):
		print " Day", day
		for c in d["specials"]:
			print "  ", c

	for day in range(0, 5):
		print_specials(day, get_daily_specials(day))

if __name__ == "__main__":
	main()

