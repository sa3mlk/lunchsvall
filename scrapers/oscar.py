#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen
from datetime import date

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
	daily_specials["specials"] = filter(len, [t.text for t in anchor.findNextSiblings("h3", limit=2)])

	try:
		for w in ["pasta", "soppa", "husman"]:
			daily_specials["specials"].append(soup.find("span", text="Veckans {}:".format(w)).next.strip())
	except AttributeError:
		pass

	return daily_specials

def main():
	import test
	test.run(get_daily_specials)

if __name__ == "__main__":
	main()

