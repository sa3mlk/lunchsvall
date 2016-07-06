#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from BeautifulSoup import BeautifulSoup, NavigableString
from urllib2 import urlopen
from datetime import date

URL = "http://svartviksherrgard.se/veckans-lunch/"

def get_daily_specials(day=None):
	page = urlopen(URL)
	soup = BeautifulSoup(page)
	page.close()

	daily_specials = {
		"name": "Svartviks Herrgård",
		"specials": [],
		"streetaddress": "Svartviksvägen 22, Kvissleby",
		"dataurl": URL,
		"mapurl=": "http://www.hitta.se/svartviks+herrgård+ab/kvissleby/zzTRP5U1Gq"
	}

	if day == None:
		day = date.today().weekday()

	if day > 4:
		return daily_specials

	days = [u"Måndag", u"Tisdag", u"Onsdag", u"Torsdag", u"Fredag"]
	day = days[day]

	span = soup.find("span", text=day)
	parent = span.findParent("div", {"class": "wpb_text_column wpb_content_element "})
	lunchdiv = parent.findNextSibling("div")
	daily_specials["specials"] = [t.text for t in lunchdiv.findAll("p")]

	return daily_specials

def main():
	import test
	test.run(get_daily_specials)

if __name__ == "__main__":
	main()

