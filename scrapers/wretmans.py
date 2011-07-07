#!/usr/bin/env python
# -*- encoding: utf8 -*-

from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen
from datetime import date
import re

URL = "http://wretmans.se/Lunchmenyer/Lunchmeny.htm"

def get_daily_specials(day=None):
	page = urlopen(URL)
	soup = BeautifulSoup(page)
	page.close()

	daily_specials = {
		"name": "Wretmans",
		"specials": [],
		"streetaddress": "Murarvägen 8, Sundsvall",
		"dataurl": URL,
		"mapurl": "http://www.hitta.se/ViewDetailsPink.aspx?Vkiid=hvjaJ0xiNoaD1S2mBsxIoA%253d%253d"
	}

	if day == None:
		day = date.today().weekday()

	# No lunch on Saturday or Sunday
	if day == 5 or day == 6:
		return daily_specials

	# Modify all the strange <span class="SpellE"> and insert a space before the text
	for s in soup.findAll("span", {"class": "SpellE"}):
		soup.find(text=s.text).replaceWith("&nbsp;" + s.text)

	day = [u"Måndag", u"Tisdag", u"Onsdag", u"Torsdag", u"Fredag"][day]
	anchor = soup.find(lambda tag: tag.name == "p" and re.match(tag.text, day))
	specials = anchor.findNextSiblings("p", limit=2)
	for i, s in enumerate([s.text for s in specials]):
		s = re.sub("\n", " ", s)
		if s[0:6] == "&nbsp;":
			daily_specials["specials"].append(s[6:])
		else:
			daily_specials["specials"].append(s)

	return daily_specials

def main():
	for day in range(5):
		d = get_daily_specials(day)
		print "%s Day %d" % (d["name"], day)
		for c in d["specials"]:
			print "  ", c

if __name__ == "__main__":
	main()

