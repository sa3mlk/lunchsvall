#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from BeautifulSoup import BeautifulSoup, NavigableString
from urllib2 import urlopen
from datetime import date
import re

URL = "http://www.mittgastronomi.com/menyer/dagenslunch"

def get_daily_specials(day=None):
	page = urlopen(URL)
	soup = BeautifulSoup(page)
	page.close()

	daily_specials = {
		"name": "Mitt Gastronomi",
		"specials": [],
		"streetaddress": "Russvägen 20, Sundsvall",
		"dataurl": URL,
		"mapurl": "http://www.hitta.se/ViewDetailsPink.aspx?Vkiid=WQ2HuqDz9prdTLqQwJejvg%253d%253d"
	}

	if day == None:
		day = date.today().weekday()

	# Only Monday - Friday
	if day > 4:
		return daily_specials

	day = [u"Måndag", u"Tisdag", u"Onsdag", u"Torsdag", u"Fredag"][day]

	anchor = soup.find("h2", text=day).findParent("tr")
	specials = anchor.findNextSibling("tr").text
	daily_specials["specials"] = filter(len, re.split("\d. ", specials))

	def split_lower_upper(s):
		start = 0
		for i, c in enumerate(s[:-1]):
			if c.islower() and s[i+1].isupper():
				stop = i+1
				yield(s[start:stop])
				start = stop
		yield s[start:]

	anchor = soup.find("h2", text="Veckans LCHF").findParent("tr")
	daily_specials["specials"].extend(split_lower_upper(anchor.findNextSibling("tr").text))

	return daily_specials

def main():
	def print_specials(day, d):
		print " Day", day
		for c in d["specials"]:
			print "  ", c

	for day in range(0, 5):
		print_specials(day, get_daily_specials(day))

if __name__ == "__main__":
	main()

