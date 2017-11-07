#!/usr/bin/env python
# -*- encoding: utf8 -*-

from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen
from datetime import date

URL = "http://tantanci.se/veckans-lunch/"

def get_daily_specials(day=None):
	page = urlopen(URL)
	soup = BeautifulSoup(page)
	page.close()

	daily_specials = {
		"name": "Tant Anci & Fröken Sara",
		"specials": [],
		"streetaddress": "Bankgatan 15, Sundsvall",
		"dataurl": URL,
		"mapurl": "https://www.hitta.se/tant+anci+och+fröken+sara/sundsvall/VSgWj-vvnO"
	}

	if day == None:
		day = date.today().weekday()

	# No lunch on Saturday or Sunday
	if day == 5 or day == 6:
		return daily_specials

	days = [u"Måndag", u"Tisdag", u"Onsdag", u"Torsdag", u"Fredag"]
	wday = days[day]
	div = soup.find("div", {"class": "entry-content"})
	p = filter(lambda t: t.text.find(wday) >= 0, div.findAll("p"))[0].text
	index = p.find(wday)
	if day < 4:
		daily_soup = p[index:p.find(days[day+1])]
		daily_specials["specials"] = [daily_soup.replace(wday, "Dagens soppa").strip()]
	else:
		daily_soup = p[index:]
		daily_specials["specials"] = [daily_soup.replace(wday, "Dagens soppa").strip()]

	return daily_specials

def main():
	import simplejson as json
	print get_daily_specials(1)["specials"][0].encode("utf8")
	#import test
	#test.run(get_daily_specials)

if __name__ == "__main__":
	main()
