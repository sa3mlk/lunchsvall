#!/usr/bin/env python
# -*- encoding: utf8 -*-

from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen
from datetime import date
import re

URL = "http://www.fernaeusgastronomiska.nu/?s=3&meny=lunch"

def get_daily_specials(day=None):
	page = urlopen(URL)
	soup = BeautifulSoup(page)
	page.close()

	daily_specials = {
		"name": "Fernaeus Gastronomiska",
		"specials": [],
		"streetaddress": "Östermovägen 37, Sundsvall",
		"dataurl": URL,
		"mapurl": "http://www.hitta.se/ViewDetailsPink.aspx?Vkiid=u028qbXr7h5QbMP0BZY59w%253d%253d&Vkid=1464367"
	}

	if day == None:
		day = date.today().weekday()

	# No lunch on Saturday or Sunday
	if day == 5 or day == 6:
		return daily_specials

	day = [u"Måndag", u"Tisdag", u"Onsdag", u"Torsdag", u"Fredag"][day]
	anchor = soup.find("b", {"class": "mark"}, text=day)
	specials = anchor.parent.findNextSibling("table").findAll("td")
	specials = [s.text for s in specials if len(s.text) > 2]

	# Add proper whitespace for e.g. "Sallad:Blabla" occurrences
	def add_proper_whitespace(m):
		s = m.group(0)
		return s[0:-1] + " " + s[-1]

	daily_specials["specials"] = map(lambda x: re.sub("\w+:[A-Z]", add_proper_whitespace, x), specials)

	return daily_specials

def main():
	for day in range(5):
		d = get_daily_specials(day)
		print "%s Day %d" % (d["name"], day)
		for c in d["specials"]:
			print "  ", c

if __name__ == "__main__":
	main()

