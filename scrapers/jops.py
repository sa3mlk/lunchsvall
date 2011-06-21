#!/usr/bin/env python
# -*- encoding: utf8 -*-

from BeautifulSoup import BeautifulSoup, NavigableString
from urllib2 import urlopen
from datetime import date

URL = "http://www.jops.se/2.html"

def get_daily_specials(day=None):
	page = urlopen(URL)
	soup = BeautifulSoup(page)
	page.close()

	daily_specials = {
		"name": "Jop's Krog",
		"specials": [],
		"streetaddress": "Trädgårdsgatan 35, Sundsvall",
		"dataurl": URL,
		"mapurl": "http://www.hitta.se/ViewDetailsPink.aspx?Vkiid=8k1vdfFFuyqG9DSKmyFgRw%253d%253d&Vkid=5147549"
	}

	if day == None:
		day = date.today().weekday()

	# No lunch on Saturday or Sunday
	if day == 5 or day == 6:
		return daily_specials

	day = [u"M&aring;ndag", u"Tisdag", u"Onsdag", u"Torsdag", u"Fredag"][day]
	day = soup.find(lambda tag: tag.name == "p" and tag.text == day)
	specials = filter(lambda x: isinstance(x, NavigableString), day.findNextSibling("p"))
	daily_specials["specials"] = [unicode(i).strip() for i in specials if len(i)]

	return daily_specials

def main():
	for day in range(5):
		d = get_daily_specials(day)
		print "%s Day %d" % (d["name"], day)
		for c in d["specials"]:
			print "  ", c

if __name__ == "__main__":
	main()

