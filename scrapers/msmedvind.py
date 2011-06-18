#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from BeautifulSoup import BeautifulSoup, NavigableString
from urllib2 import urlopen
from datetime import date
import re

URL = "http://www.msmedvind.com/meny/"

def get_daily_specials(day=None):
	page = urlopen(URL)
	soup = BeautifulSoup(page)
	page.close()

	daily_specials = {
		"name": "M/S Medvind",
		"specials": [],
		"streetaddress": "Inre hamnen i Sundsvall",
		"dataurl": URL,
		"mapurl": "http://www.hitta.se/ViewDetailsPink.aspx?Vkiid=O8TtXChV4EsiSHvMTwKX5A%253d%253d"
	}

	if day == None:
		day = date.today().weekday()

	# Only Monday - Friday
	if day > 4:
		return daily_specials

	day = [u"M&aring;ndag:", u"Tisdag:", u"Onsdag:", u"Torsdag:", u"Fredag:"][day]
	pattern = re.compile(day)
	daily = soup.find(lambda tag: tag.name == "span" and re.match(pattern, tag.text))

	if len(daily.text) > len(day):
		daily = str(daily.text[len(day):]).strip()
	else:
		special = daily.findNextSiblings("span", limit=1)
		daily = str(special[0].text).strip()

	stop = daily.find("Alltid ombord:")
	if stop > 0:
		daily = daily[:stop]

	daily_specials["specials"].append(daily)

	return daily_specials

def main():
	def print_specials(day, d):
		print " Day", day
		for c in d["specials"]:
			print "  ", c
		print ""

	d = get_daily_specials(0)
	print d["name"]
	print_specials(0, d)
	for day in range(1, 5):
		print_specials(day, get_daily_specials(day))

if __name__ == "__main__":
	main()

