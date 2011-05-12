#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen
from datetime import date

URL = "http://www.sidsjohotell.se/restaurang-gardshuset/meny/"

def get_daily_specials(day=None):
	page = urlopen(URL)
	soup = BeautifulSoup(page)
	page.close()

	daily_specials = {"name": u"Restaurang Gårdshuset", "specials": []}
	if day == None:
		day = date.today().weekday()

	# Only Monday - Friday
	if day > 4:
		return daily_specials

	day = [u"Måndag", u"Tisdag", u"Onsdag", u"Torsdag", u"Fredag"][day]
	menu = soup.find("div", {"class": "entry-content"})
	day = menu.find("strong", text=day)
	daily_specials["specials"] = [unicode(day.next.next.next)]

	return daily_specials

def main():
	for day in range(5):
		d = get_daily_specials(day)
		print d["name"]
		for c in d["specials"]:
			print "  ", c

if __name__ == "__main__":
	main()

