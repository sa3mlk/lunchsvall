#!/usr/bin/env python
# -*- encoding: utf8 -*-

from BeautifulSoup import BeautifulSoup, NavigableString
from urllib2 import urlopen
from datetime import date
import re

URL = "http://delicerano.se/lunch.htm"

def get_daily_specials(day=None):
	page = urlopen(URL)
	soup = BeautifulSoup(page)
	page.close()

	daily_specials = {
		"name": "Delicerano",
		"specials": [],
		"streetaddress": "Sjögatan 7, Sundsvall",
		"dataurl": URL,
		"mapurl": "http://www.hitta.se/ViewDetailsPink.aspx?Vkiid=BjgBy%2bYy%252fc3YvyHSBs8Xeg%253d%253d&Vkid=2856959"
	}

	if day == None:
		day = date.today().weekday()

	# No lunch on Saturday or Sunday
	if day == 5 or day == 6:
		return daily_specials

	day = [u"M&Aring;NDAG", u"TISDAG", u"ONSDAG", u"TORSDAG", u"FREDAG"][day]
	pattern = re.compile(day, re.IGNORECASE)
	day = soup.find(lambda tag: tag.name == "span" and pattern.match(tag.text))

	specials = []
	siblings = day.findAllNext(lambda t: t.name == "p" and len(t.text), limit=4)
	for sibling in siblings:
		if len(specials) == 4:
			break
		for element in sibling:
			if isinstance(element, NavigableString):
				specials.append(str(element))
				if len(specials) == 4:
					break

	daily_specials["specials"] = specials
	return daily_specials

def main():
	def print_specials(day, d):
		print "Day", day
		for c in d["specials"]:
			print u'  ', c

	d = get_daily_specials(0)
	print d["name"]
	print_specials(0, d)
	for day in range(1, 5):
		print_specials(day, get_daily_specials(day))

if __name__ == "__main__":
	main()

