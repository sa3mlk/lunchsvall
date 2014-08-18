#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from BeautifulSoup import BeautifulSoup, NavigableString, Tag
from urllib2 import urlopen
from datetime import date
import re

URL = "http://www.oscarmatsal.se/matsal/"

def get_daily_specials(day=None):
	page = urlopen(URL)
	soup = BeautifulSoup(page)
	page.close()

	daily_specials = {
		"name": "Oscar Matsal & Bar",
		"specials": [],
		"streetaddress": "Bankgatan 1, Sundsvall",
		"dataurl": URL,
		"mapurl": "http://www.hitta.se/oscar+matsal+och+bar/sundsvall/xSR2wmOOOU"
	}

	if day == None:
		day = date.today().weekday()

	# Only Monday - Friday
	if day > 4:
		return daily_specials

	day = [u"Måndag", u"Tisdag", u"Onsdag", u"Torsdag", u"Fredag"][day]
	anchor = soup.find(lambda tag: tag.name == "h1" and tag.text == day and tag["class"] == "lunch")
	daily_specials["specials"] = [t.text for t in anchor.findNextSiblings("h3", limit=2)]

	for w in ["pasta", "soppa", "sallad"]:
		daily_specials["specials"].append(soup.find("span", text="Veckans {}:".format(w)).next.strip())

	return daily_specials

def main():
	def print_specials(day, d):
		print " Day", day
		for c in d["specials"]:
			print "  ", c
		print ""

	for day in range(0, 5):
		print_specials(day, get_daily_specials(day))

if __name__ == "__main__":
	main()

