#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from BeautifulSoup import BeautifulSoup, NavigableString, Tag
from urllib2 import urlopen
from datetime import date
import re

URL = "http://www.skonerten.se/"

def get_daily_specials(day=None):
	page = urlopen(URL)
	soup = BeautifulSoup(page)
	page.close()

	daily_specials = {
		"name": "Skonerten",
		"specials": [],
		"streetaddress": "Packhusgatan 4, Sundsvall",
		"dataurl": URL,
		"mapurl": "http://www.hitta.se/ViewDetailsPink.aspx?Vkiid=11IAWjLqMBv1aPZn4Dip9g%253d%253d&Vkid=1456953"
	}

	if day == None:
		day = date.today().weekday()

	# Only Monday - Friday
	if day > 4:
		return daily_specials

	def process_tags(contents):
		s = "".join(map(lambda x: x.text, filter(lambda x: isinstance(x, Tag), contents)))
		s = filter(len, map(lambda s: s.strip(), re.split("\.", s)))
		return s

	def process_strings(contents):
		s = filter(len, map(lambda x: str(x).strip(), filter(lambda x: isinstance(x, NavigableString), contents)))
		return s

	def food_filter(contents):
		# First try to extract the strings
		s = process_strings(contents)
		if not len(s):
			# But sometimes they have non-closed <b> tags around the specials
			return process_tags(contents)
		else:
			return s

	# Get all TDs with the following attributes
	match = {"height": "50", "align": "left", "width": "50%"}
	tds = soup.findAll("td", match)
	daily_specials["specials"] = food_filter(tds[day].find("font").contents)

	# ... and all daily soups
	match["width"] = "30%"
	tds = soup.findAll("td", match)
	daily_specials["specials"] += food_filter(tds[day].find("font").contents)

	return daily_specials

def main():
	for day in range(5):
		d = get_daily_specials(day)
		print "%s Day %d" % (d["name"], day)
		for c in d["specials"]:
			print "  ", c

if __name__ == "__main__":
	main()

