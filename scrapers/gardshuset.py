#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from BeautifulSoup import BeautifulSoup, NavigableString
from urllib2 import urlopen
from datetime import date

URL = "http://www.sidsjohotell.se/restaurang-gardshuset/meny/"

def get_daily_specials():
	#page = urlopen(URL)
	#soup = BeautifulSoup(page)
	#page.close()

	soup = BeautifulSoup(open("gardshuset.html"))

	daily_specials = {"name": "Restaurang Gårdshuset", "specials": []}
	day = date.today().weekday()

	# Only Monday - Friday
	if day > 4:
		return daily_specials

	day = [u"Måndag", u"Tisdag", u"Onsdag", u"Torsdag", u"Fredag"][day]
	print day

	menu = soup.find("div", {"class": "entry-content"})
	print menu.prettify()

	'''day = soup.find("h3", text=day)
	parent = day.findParent("tr")
	td = parent.findChild("td", valign="top")

	# Filter out the strings only
	daily_specials["specials"] = [str(c) for c in
		filter(lambda x: isinstance(x, NavigableString), td.contents)]'''

	return daily_specials

def main():
	d = get_daily_specials()
	print d["name"]
	for c in d["specials"]:
		print "  ", c

if __name__ == "__main__":
	main()

