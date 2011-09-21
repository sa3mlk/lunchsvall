#!/usr/bin/env python
# -*- encoding: utf8 -*-

from BeautifulSoup import BeautifulSoup, NavigableString, Tag
from urllib2 import urlopen
from datetime import date
import re

URL = "http://aglantan.se/LUNCH.htm"

def get_daily_specials(day=None):
	page = urlopen(URL)
	soup = BeautifulSoup(page)
	page.close()

	daily_specials = {
		"name": u"Ågläntan",
		"specials": [],
		"streetaddress": "Skepparegatan 11, Sundsvall",
		"dataurl": URL,
		"mapurl": "http://www.hitta.se/ViewDetailsPink.aspx?Vkiid=aEQ2w9zT%252fjfOvsd7%2bmgJfw%253d%253d"
	}

	if day == None:
		day = date.today().weekday()

	# No lunch on Saturday or Sunday
	if day == 5 or day == 6:
		return daily_specials

	day = [u"M&aring;ndag", u"Tisdag", u"Onsdag", u"Torsdag", u"Fredag"][day]
	day = soup.find(lambda tag: tag.name == "strong" and day in tag.contents)

	specials = []
	for i in range(4):
		if not day.nextSibling:
			day = day.parent
		day = day.nextSibling
		if not day:
			break
		if isinstance(day, NavigableString):
			specials.append(day.strip())
		elif isinstance(day, Tag):
			specials.append(day.text.strip())

	# Ugly special case
	def join_if_lowercase(s):
		s = filter(lambda x: len(x) > 0, s)
		if len(s) > 1 and len(s[1]) > 2 and s[1][0].islower():
			return [s[0] + " " + s[1]]
		else:
			return s[:1]

	specials = join_if_lowercase(specials)

	# Hardcoded for now, very ugly indeed.
	specials.append(u"Caesarsallad med kyckling bacon & dressing 99 kr")

	daily_specials["specials"] = specials

	return daily_specials

def main():
	def print_specials(day, d):
		print "Day", day
		for c in d["specials"]:
			print "  ", c

	d = get_daily_specials(0)
	print d["name"]
	print_specials(0, d)
	for day in range(1, 5):
		print_specials(day, get_daily_specials(day))

if __name__ == "__main__":
	main()

