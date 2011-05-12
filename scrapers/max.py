#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from BeautifulSoup import BeautifulSoup, NavigableString
from urllib2 import urlopen
from datetime import date

URL = "http://www.max.se/maten.aspx"

def get_daily_specials():
	page = urlopen(URL)
	soup = BeautifulSoup(page)

	daily_specials = {"name": "mAx", "specials": []}
	day = date.today().weekday()

	# Only Monday - Friday
	if day > 4:
		return daily_specials

	h2 = soup.find("h2", text="Dagens lunch 10-14")
	table = h2.parent.findNextSibling("table")

	today = []
	for td in table.findAll("td"):
		today.append(filter(lambda x: isinstance(x, NavigableString), td.contents)[day])

	daily_specials["specials"].append(unicode(today[1].replace(u"Ã¥", u"å")))
	return daily_specials

def main():
	d = get_daily_specials()
	print d["name"]
	for c in d["specials"]:
		print "  ", c

if __name__ == "__main__":
	main()

