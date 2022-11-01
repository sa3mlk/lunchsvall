#!/usr/bin/env python
# -*- encoding: utf8 -*-

from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
from datetime import date

URL = "http://www.norrlandskallaren.nu/lunch"

def get_daily_specials(day=None):
	page = urlopen(URL)
	soup = BeautifulSoup(page)
	page.close()

	daily_specials = {
		"name": "Norrlandskällaren",
		"specials": [],
		"streetaddress": "Storgatan 18, Sundsvall",
		"dataurl": URL,
		"mapurl": "http://gulasidorna.eniro.se/f/norrlandsk%C3%A4llaren:14372050"
	}

	if day == None:
		day = date.today().weekday()

	# Only Monday - Friday
	if day > 4:
		return daily_specials

	day = [u"måndag", u"tisdag", u"onsdag", u"torsdag", u"fredag"][day]
	pattern = re.compile("^" + day + ":", re.IGNORECASE)
	today = soup.find(lambda tag: tag.name == "p" and pattern.match(tag.text))

	# No match, abort
	if not today:
		return daily_specials

	for s in today.findNextSiblings("p", limit=3):
		daily_specials["specials"].append(s.text.replace("\r\n", " "))

	return daily_specials

def main():
	for day in range(5):
		d = get_daily_specials(day)
		print("Day", day)
		if len(d["specials"]) == 0:
			continue
		else:
			for c in d["specials"]:
				print(" ", c)

if __name__ == "__main__":
	main()
