#!/usr/bin/env python
# -*- encoding: utf8 -*-

from BeautifulSoup import BeautifulSoup, Tag
from urllib2 import urlopen
from datetime import date

URL = "http://www.kalabra.nu/"

def get_daily_specials(day=None):
	page = urlopen(URL)
	soup = BeautifulSoup(page)
	page.close()

	daily_specials = {
		"name": "Kalabra",
		"specials": [],
		"streetaddress": "Fridhemsgatan 136",
		"dataurl": URL,
		"mapurl": "http://www.hitta.se/kalabra-kubenbadet/sundsvall/ySjXGkAeeu"
	}

	if day == None:
		day = date.today().weekday()

	# No lunch on Saturday or Sunday
	if day == 5 or day == 6:
		return daily_specials

	day = [u"Måndag", u"Tisdag", u"Onsdag", u"Torsdag", u"Fredag"][day]

	parent = soup.find("h2", text=day).parent
	daily_specials["specials"].append(parent.findNextSibling("p").text)

	return daily_specials

def main():
	for day in range(5):
		d = get_daily_specials(day)
		print "%s Day %d" % (d["name"], day)
		for c in d["specials"]:
			print "  ", c

if __name__ == "__main__":
	main()

