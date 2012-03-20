#!/usr/bin/env python
# -*- encoding: utf8 -*-

from BeautifulSoup import BeautifulSoup, NavigableString
from urllib2 import urlopen
from datetime import date
import re

URL = "http://www.opuspianobar.se/?page_id=966"

def get_daily_specials(day=None):
	page = urlopen(URL)
	soup = BeautifulSoup(page)
	page.close()

	daily_specials = {
		"name": "Opus Restaurang & Pianobar",
		"specials": [],
		"streetaddress": "Storgatan 12, Sundsvall",
		"dataurl": URL,
		"mapurl": "http://www.hitta.se/ViewDetailsPink.aspx?Vkiid=NrPzwEi7q6HH1xb0FCnsnA%253d%253d&Vkid=5745344"
	}

	if day == None:
		day = date.today().weekday()

	# No lunch on Saturday or Sunday
	if day == 5 or day == 6:
		return daily_specials

	day = [u"Måndag:", u"Tisdag:", u"Onsdag:", u"Torsdag:", u"Fredag"][day]
	pattern = re.compile(day, re.IGNORECASE)
	day = soup.find(lambda tag: tag.name == "strong" and pattern.match(tag.text))

	specials = []
	for i in range(8):
		day = day.nextSibling
		if not day or len(specials) == 2:
			break
		if isinstance(day, NavigableString):
			specials.append(day.strip())
	
	daily_specials["specials"] = specials
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

