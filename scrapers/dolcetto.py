#!/usr/bin/env python
# -*- encoding: utf8 -*-

from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen
from datetime import date
import re

URL = "http://www.dolcetto.nu/Veckolunchmeny.htm"

def get_daily_specials(day=None):
	page = urlopen(URL)
	soup = BeautifulSoup(page)
	page.close()

	daily_specials = {
		"name": "Dolcetto",
		"specials": [],
		"streetaddress": "Kyrkogatan 8, Sundsvall",
		"dataurl": URL,
		"mapurl": "http://www.hitta.se/ViewDetailsPink.aspx?Vkiid=4uG7%252fiYMOcHQKtp0VSkMNw%253d%253d&Vkid=3215131"
	}

	if day == None:
		day = date.today().weekday()

	# No lunch on Saturday or Sunday
	if day == 5 or day == 6:
		return daily_specials

	day = [u"M&aring;ndag", u"Tisdag", u"Onsdag", u"Torsdag", u"Fredag"][day]

	pattern = re.compile(day, re.IGNORECASE)
	day = soup.find(lambda tag: tag.name == "p" and pattern.match(tag.text))
	daily_specials["specials"] = [day.findNextSibling(lambda t: t.name == "p" and len(t.text)).text.strip()]

	return daily_specials

def main():
	for day in range(5):
		d = get_daily_specials(day)
		print "%s Day %d" % (d["name"], day)
		for c in d["specials"]:
			print "  ", c

if __name__ == "__main__":
	main()

