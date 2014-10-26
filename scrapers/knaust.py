#!/usr/bin/env python
# -*- encoding: utf8 -*-

from BeautifulSoup import BeautifulSoup, Tag
from urllib2 import urlopen
from datetime import date
import re

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

	search_items = [day, "Veckans fisk", "Veckans pasta", "Sallad"]
	for i in search_items:
		anchor = soup.find("strong", text=i)
		daily_specials["specials"].extend(anchor.findAllNext(text=True, limit=1))

	return daily_specials

def main():
	for day in range(5):
		d = get_daily_specials(day)
		print "%s Day %d" % (d["name"], day)
		for c in d["specials"]:
			print "  ", c

if __name__ == "__main__":
	main()

