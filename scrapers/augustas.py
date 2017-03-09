#!/usr/bin/env python
# -*- encoding: utf8 -*-

from BeautifulSoup import BeautifulSoup, NavigableString
from urllib2 import urlopen
from datetime import date

URL = "http://www.baltichotell.com/lunch.aspx"

def get_daily_specials(day=None):
	page = urlopen(URL)
	soup = BeautifulSoup(page)
	page.close()

	daily_specials = {
		"name": "Augustas Kök",
		"specials": [],
		"streetaddress": "Sjögatan 5, Sundsvall",
		"dataurl": URL,
		"mapurl": "https://www.hitta.se/best+western+hotel+baltic/sundsvall/hglwn1bJJA"
	}

	if day == None:
		day = date.today().weekday()

	# No lunch on Saturday or Sunday
	if day == 5 or day == 6:
		return daily_specials

	days = [u"M&aring;ndag", u"Tisdag", u"Onsdag", u"Torsdag", u"Fredag"]
	wday = days[day]

	def findSpecial(name):
		def findNextString(tag):
			return tag.replace("&nbsp;", "").strip() if isinstance(tag, NavigableString) and len(tag) > 1 else findNextString(tag.next)
		strong = soup.find("strong", text=name)
		return findNextString(strong.next)

	specials = [("Dagens", wday), ("Fisk", "Veckans Fisk &nbsp;&nbsp;&nbsp;&nbsp;"), ("Gryta", "Veckans gryta"), ("Vegetarisk", "Veckans vegetariska"), ("Sallad", "Veckans sallad &nbsp;&nbsp;&nbsp;&nbsp;")]
	daily_specials["specials"] = [t + ": " + findSpecial(s) for t, s in specials]

	return daily_specials

def main():
	import test
	test.run(get_daily_specials)

if __name__ == "__main__":
	main()
