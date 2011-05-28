#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen
from datetime import date

URL = "http://kampanjsajt.nu/st/lunchguiden/"

def get_daily_specials():
	page = urlopen(URL)
	soup = BeautifulSoup(page)
	page.close()

	restaurants = [(i.text, i["href"][1:]) for i in
		soup.find("div", id="menu").findChildren("a", {"class": "block"})]

	daily_specials = []

	# No lunch on Saturday or Sunday
	day = date.today().weekday()
	if day == 5 or day == 6:
		return daily_specials

	for r in restaurants:
		def specials():
			# Return a list of all specials for the given restaurant by its link reference
			div = soup.find("a", {"class": "ref", "name": r[1]})
			ul = div.parent.find("ul")
			# Return an empty list if there are no daily specials available, otherwise
			# all <li> tags in the list
			return [li.text for li in ul] if ul else []
		s = specials()
		if len(s):
			daily_specials.append({"name": r[0], "specials": s})

	return daily_specials

def main():
	for d in get_daily_specials():
		print d["name"].encode("UTF-8")
		for c in d["specials"]:
			print "  ", c.encode("UTF-8")

if __name__ == "__main__":
	main()

