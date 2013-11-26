#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from BeautifulSoup import BeautifulSoup, NavigableString
from urllib2 import urlopen
from datetime import date

URL = "http://sundsvall.invitobar.se/?page_id=1038"

def get_daily_specials(day=None):
	page = urlopen(URL)
	soup = BeautifulSoup(page)
	page.close()

	daily_specials = {
		"name": "Invito",
		"specials": [],
		"streetaddress": "Storgatan 6-8, Sundsvall",
		"dataurl": URL,
		"mapurl": "http://www.hitta.se/ViewDetailsPink.aspx?Vkiid=h7sTX8JwG1d8a10%252fW3RuwA%253d%253d&Vkid=2688685"
	}

	day = date.today().weekday() if day is None else day

	# Only Monday - Friday
	if day > 4:
		return daily_specials

	day = [u"MÅNDAG", u"TISDAG", u"ONSDAG", u"TORSDAG", u"FREDAG"][day]
	day = soup.find("h2", text=day)
	specials = filter(lambda tag: isinstance(tag, NavigableString), day.findNext("p").contents)
	daily_specials["specials"] = [s.strip() for s in specials]

	return daily_specials

def main():
	for day in range(5):
		d = get_daily_specials(day)
		print "Day {day} at {name}".format(day=day, name=d["name"])
		for c in d["specials"]:
			print "  ", c

if __name__ == "__main__":
	main()

