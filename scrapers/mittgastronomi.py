#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from BeautifulSoup import BeautifulSoup, NavigableString
from urllib2 import urlopen
from datetime import date
import re

URL = "http://www.mittgastronomi.com/blogg/?page_id=4"

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

	day = [u"Måndag:", u"Tisdag:", u"Onsdag:", u"Torsdag:", u"Fredag:"][day]

	def get_specials(match):
		specials = []
		pattern = re.compile(match)
		day = soup.find(lambda tag: tag.name == "strong" and re.match(pattern, tag.text))
		next = day.next.next
		while True:
			if isinstance(next, NavigableString):
				s = str(next).strip()
				if len(s) > 3:
					specials.append(s[3:])
			else:
				if next.name == "p":
					next = None
			if next:
				next = next.next
			else:
				break
		return specials

	daily_specials["specials"].extend(get_specials(day))
	daily_specials["specials"].extend(get_specials("Hela veckan:"))

	return daily_specials

def main():
	def print_specials(day, d):
		print " Day", day
		for c in d["specials"]:
			print "  ", c
		print ""

	d = get_daily_specials(0)
	print d["name"]
	print_specials(0, d)
	for day in range(1, 5):
		print_specials(day, get_daily_specials(day))

if __name__ == "__main__":
	main()

