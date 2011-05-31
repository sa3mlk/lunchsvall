#!/usr/bin/env python
# -*- encoding: utf8 -*-

from BeautifulSoup import BeautifulSoup, NavigableString
from urllib2 import urlopen
from datetime import date
import re

URL = "http://delicerano.se/Lunch.html"

def get_daily_specials(day=None):
	page = urlopen(URL)
	soup = BeautifulSoup(page)
	page.close()

	daily_specials = {
		"name": "Delicerano",
		"specials": [],
		"streetaddress": "Sjögatan 7, Sundsvall",
		"mapurl": "http://www.hitta.se/ViewDetailsPink.aspx?Vkiid=BjgBy%2bYy%252fc3YvyHSBs8Xeg%253d%253d&Vkid=2856959"
	}

	if day == None:
		day = date.today().weekday()

	# No lunch on Saturday or Sunday
	if day == 5 or day == 6:
		return daily_specials

	day = [u"m&aring;ndag", u"tisdag", u"onsdag", u"torsdag", u"fredag"][day]

	def fix_html(s):
		# TODO: You might add more special html characters here
		chars = [(u"&amp;", u"&"), (u"&nbsp;", u" "), (u"&auml;", u"ä"),
				 (u"&Auml;", u"Ä"), (u"&ouml;", u"ö"), (u"&Ouml;", u"Ö"),
				 (u"&aring;", u"å"), (u"&Aring;", u"Å"), (u"&eacute;", u"é"),
				 (u"&egrave;", u"è")]
		for html, char in chars:
			s = s.replace(html, char)
		return s

	def add_missing_spaces(s):
		# Ugly patch
		if s.find("VECKANS MENY") != -1:
			return ""
		n = ""
		for i, c in enumerate(s[0:-1]):
			n += c
			if s[i + 1].isupper() and c.islower():
				n += " "
		return n + s[-1]

	def fix_string(s):
		return add_missing_spaces(fix_html(s))

	pattern = re.compile(day, re.IGNORECASE)
	day = soup.find(lambda tag: tag.name == "h2" and pattern.match(tag.text))
	# FIXME: Sometimes two or more dishes share the same <p> tag; split them on "%d kr" perhaps?
	siblings = day.findNextSiblings(lambda t: t.name == "p" and len(t.text), limit=4)
	daily_specials["specials"] = filter(lambda x: len(x), map(lambda x: fix_string(x.text.strip()), siblings))

	return daily_specials

def main():
	for day in range(5):
		d = get_daily_specials(day)
		print d["name"]
		for c in d["specials"]:
			print "  ", c

if __name__ == "__main__":
	main()

