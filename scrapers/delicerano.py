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
		"dataurl": URL,
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
			if s[i + 1].isupper() and c.islower() or c == '.':
				n += " "
		return n + s[-1]

	def split_on_price(s):
		return filter(lambda s: len(s), map(lambda s: s.strip(), re.split("\d+.kr",s)))

	def fix_string(s):
		return split_on_price(add_missing_spaces(fix_html(s)))

	pattern = re.compile(day, re.IGNORECASE)
	day = soup.find(lambda tag: tag.name == "h2" and pattern.match(tag.text))
	siblings = day.findNextSiblings(lambda t: t.name == "p" and len(t.text), limit=3)

	specials = []
	for special in filter(lambda x: len(x), map(lambda x: fix_string(x.text.strip()), siblings)):
		specials.extend(special)

	daily_specials["specials"] = specials[0:4]

	return daily_specials

def main():
	def print_specials(day, d):
		print "Day", day
		for c in d["specials"]:
			print "  ", c

	d = get_daily_specials(0)
	print d["name"]
	print_specials(0, d)
	for day in range(1, 5):
		print_specials(day, get_daily_specials(day))

if __name__ == "__main__":
	main()

