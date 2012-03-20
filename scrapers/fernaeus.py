#!/usr/bin/env python
# -*- encoding: utf8 -*-

from BeautifulSoup import BeautifulSoup, Tag
from urllib2 import urlopen
from datetime import date
import re

URL = "http://www.fernaeusgastronomiska.nu/menyer/veckans-lunch.aspx"

def get_daily_specials(day=None):
	page = urlopen(URL)
	soup = BeautifulSoup(page)
	page.close()

	daily_specials = {
		"name": "Fernaeus Gastronomiska",
		"specials": [],
		"streetaddress": "Östermovägen 37, Sundsvall",
		"dataurl": URL,
		"mapurl": "http://www.hitta.se/ViewDetailsPink.aspx?Vkiid=u028qbXr7h5QbMP0BZY59w%253d%253d&Vkid=1464367"
	}

	if day == None:
		day = date.today().weekday()

	# No lunch on Saturday or Sunday
	if day == 5 or day == 6:
		return daily_specials

	day = [u"Måndag", u"Tisdag", u"Onsdag", u"Torsdag", u"Fredag"][day]

	parent = soup.find("h2", text=day).parent
	lis = parent.findNextSibling("ul").findAll("li", limit=3)
	daily_specials["specials"] = [t.text[2:] for t in lis]

	return daily_specials

def main():
	for day in range(5):
		d = get_daily_specials(day)
		print "%s Day %d" % (d["name"], day)
		for c in d["specials"]:
			print "  ", c

if __name__ == "__main__":
	main()

