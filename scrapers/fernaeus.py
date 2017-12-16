#!/usr/bin/env python
# -*- encoding: utf8 -*-

from BeautifulSoup import BeautifulSoup, Tag
from urllib2 import urlopen
from datetime import date

URL = "http://www.fernaeusgastronomiska.nu/"

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

	weekday = soup.findAll("div", {"class": "col weekday bummer"})[day]
	daily_specials["specials"] = [t.text.strip() for t in weekday.findAll("p")]

	return daily_specials

def main():
	import test
	test.run(get_daily_specials)

if __name__ == "__main__":
	main()

