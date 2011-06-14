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
	siblings = day.findNextSiblings(lambda t: t.name == "p" and len(t.text), limit=2)

	specials = filter(lambda x: len(x), map(lambda x: x.text.strip(), siblings))
	# Join strings where the string begin with a lower case character
	for i, s in enumerate(specials):
		if s[0].islower():
			specials[i - 1] += " %s" % s

	# Delete all strings that only contains "&nbsp;" or begin with a lower case character
	daily_specials["specials"] = filter(lambda s: s[0].isupper() and s != "&nbsp;", specials)
	return daily_specials

def main():
	for day in range(5):
		d = get_daily_specials(day)
		print "%s Day %d" % (d["name"], day)
		for c in d["specials"]:
			print "  ", c

if __name__ == "__main__":
	main()

