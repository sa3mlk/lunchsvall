#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from BeautifulSoup import BeautifulSoup, NavigableString
from urllib2 import urlopen
from datetime import date
import re

URL = "http://laco.se/lunch/"

def get_daily_specials(day=None):
	page = urlopen(URL)
	soup = BeautifulSoup(page)
	page.close()

	daily_specials = {
		"name": "Laco di Como",
		"specials": [],
		"streetaddress": "Timmervägen 6, Sundsvall",
		"dataurl": URL,
		"mapurl": "http://www.hitta.se/ViewDetailsPink.aspx?Vkiid=VgwibzXcvb%252fAf1XfiCvetg%253d%253d"
	}

	if day == None:
		day = date.today().weekday()

	# Only Monday - Friday
	if day > 4:
		return daily_specials

	day = [u"Måndag", u"Tisdag", u"Onsdag", u"Torsdag", u"Fredag"][day]

	div = soup.find("p", text=day).parent.findNextSibling("div", id=34)
	daily_specials["specials"] = [l.text for l in div.ul.findAll("li")]

	def split_items(s):
		return map(lambda x: x.replace("\n", "").strip(), filter(lambda y: isinstance(y, NavigableString), s.contents))

	items = [(u"Sallad", u"Sallad"), (u"Pasta", u"Pasta")]
	daily_specials["specials"].extend([t[0] + ": " + ". ".join(split_items(soup.find("h2", text=t[1]).parent.findNextSibling("p"))) for t in items])

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

