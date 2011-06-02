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

	daily_specials = {
		"name": u"Restaurang Gårdshuset",
		"specials": [],
		"streetaddress": "Arthur Engbergs Väg 11, Sundsvall",
		"mapurl": "http://www.hitta.se/ViewDetailsPink.aspx?Vkiid=ww6BfFoSzg9YJaefKRj2tQ%253d%253d&Vkid=2670064"
	}

	if day == None:
		day = date.today().weekday()

	# Only Monday - Friday
	if day > 4:
		return daily_specials

	today = soup.find("span", id=str(day))
	if today:
		daily_specials["specials"] = [today.contents[0]]

	return daily_specials

def main():
	for day in range(5):
		d = get_daily_specials(day)
		if len(d["specials"]) == 0:
			continue
		print "%s | day %d" % (d["name"], day)
		for c in d["specials"]:
			print "  ", c

if __name__ == "__main__":
	main()

