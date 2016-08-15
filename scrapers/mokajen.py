#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from BeautifulSoup import BeautifulSoup, NavigableString
from urllib2 import urlopen
from datetime import date
import re

URL = "http://mittgastronomi.com/lunch-mokajen/"

def get_daily_specials(day=None):
	page = urlopen(URL)
	soup = BeautifulSoup(page)
	page.close()

	daily_specials = {
		"name": "Mokajen",
		"specials": [],
		"streetaddress": "Kolvägen 9, Sundsvall",
		"dataurl": URL,
		"mapurl": "http://www.hitta.se/restaurang+mokajen/sundsvall/xWPjss5Xvm"
	}

	if day == None:
		day = date.today().weekday()

	if day > 4:
		return daily_specials

	day = [u"MÅNDAG", u"TISDAG", u"ONSDAG", u"TORSDAG", u"FREDAG"][day]
	day_td = soup.find("td", text=day)

	table = day_td.findParent("table")
	tbody = table.find("tbody")
	specials = filter(lambda t: isinstance(t, NavigableString), tbody.findAll("tr")[1].td.contents)
	for s in specials:
		daily_specials["specials"].append(re.sub(r'\([^)]*\)', '\n', s).strip())

	return daily_specials

def main():
	import test
	test.run(get_daily_specials)

if __name__ == "__main__":
	main()

