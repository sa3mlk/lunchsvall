#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen

URL = "http://kampanjsajt.nu/st/lunchguiden/"

def get_daily_specials():
	page = urlopen(URL)
	soup = BeautifulSoup(page)

	restaurants = []

	menu = soup.find("div", id="menu")
	for i in menu.findChildren("a", {"class": "block"}):
		# Save the name of the place and the link reference
		restaurants.append((i.text, i["href"][1:]))

	daily_specials = []

	for r in restaurants:
		def specials():
			# Return a list of all specials for the given restaurant by its link reference
			div = soup.find("a", {"class": "ref", "name": r[1]})
			return [li.text for li in div.parent.find("ul")]
		daily_specials.append({"name": r[0], "specials": specials()})

	return daily_specials

def main():
	for d in get_daily_specials():
		print d["name"].encode("UTF-8")
		for c in d["specials"]:
			print "  ", c.encode("UTF-8")

if __name__ == "__main__":
	main()

