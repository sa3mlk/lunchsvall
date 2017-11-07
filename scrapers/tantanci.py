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

	days = [u"ndag", u"Tisdag", u"Onsdag", u"Torsdag", u"Fredag"]
	wday = days[day]
	div = soup.find("div", {"class": "entry-content"})
	try:
		p = filter(lambda t: t.text.find(wday) >= 0, div.findAll("p"))[0].text
	except IndexError:
		return daily_specials

	index = p.find(wday)
	if day < 4:
		daily_soup = p[index:p.find(days[day+1])]
		daily_specials["specials"] = [daily_soup.replace(wday, "Dagens soppa")]
	else:
		daily_soup = p[index:]
		daily_specials["specials"] = [daily_soup.replace(wday, "Dagens soppa")]

	# Quick and dirty patch for Swedish characters.
	def fix_string(s):
		return s.replace(u"ĂĽ", u"å").replace(u"Ăś", u"ö").replace(u"Ă¤", u"ä").replace(u"Â", "").strip()

	daily_specials["specials"] = [fix_string(x) for x in daily_specials["specials"]]

	return daily_specials

def main():
	import test
	test.run(get_daily_specials)

if __name__ == "__main__":
	main()
