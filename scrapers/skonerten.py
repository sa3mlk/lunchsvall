#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from BeautifulSoup import BeautifulSoup, NavigableString
from urllib2 import urlopen
from datetime import date

URL = "http://www.skonerten.se/"

def get_daily_specials():
	page = urlopen(URL)
	soup = BeautifulSoup(page)

	daily_specials = {"name": "Skonerten", "specials": []}
	day = date.today().weekday()

	# Only Monday - Friday
	if day > 4:
		return daily_specials

	def food_filter(contents):
		return map(lambda x: str(x).strip(),
			filter(lambda x: isinstance(x, NavigableString), contents))

	# Get all TDs with the following attributes
	match = {"height": "50", "align": "left", "width": "50%"}
	tds = soup.findAll("td", match)
	daily_specials["specials"] = food_filter(tds[day].find("font").contents)

	# ... and all daily soups
	match["width"] = "30%"
	tds = soup.findAll("td", match)
	daily_specials["specials"] += food_filter(tds[day].find("font").contents)

	return daily_specials

def main():
	d = get_daily_specials()
	print d["name"]
	for c in d["specials"]:
		print "  ", c

if __name__ == "__main__":
	main()

