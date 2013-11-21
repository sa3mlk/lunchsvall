#!/usr/bin/env python
# -*- encoding: utf-8 -*-

URL = "http://www.estreet.nu"

def get_daily_specials(day=None):
	from BeautifulSoup import BeautifulSoup
	from urllib2 import urlopen
	from datetime import date

	day = date.today().weekday() if day is None else day

	daily_specials = {
		"name": "E-street",
		"specials": [],
		"streetaddress": "Esplanaden 14, Sundsvall",
		"dataurl": URL,
		"mapurl": "http://www.hitta.se/e+street/sundsvall/zzzRPjw5X4?vad=e-street&var=sundsvall"
	}

	try:
		day = [u"Måndag", u"Tisdag", u"Onsdag", u"Torsdag", u"Fredag"][day]
	except IndexError:
		return daily_specials

	page = urlopen(URL)
	soup = BeautifulSoup(page)
	page.close()

	div = soup.find("div", id="gg_lunch_widget-3")

	def find_specials(match):
		day_title = div.find(lambda tag: tag.name == "h6" and tag.text == match)
		specials = day_title.findNext("p").text
		return filter(len, specials.split("\r\n"))

	patterns = [day, "Veckans soppa", "Veckans sallad"]
	for p in patterns:
		daily_specials["specials"] += find_specials(p)

	return daily_specials

def main():
	for i in range(5):
		d = get_daily_specials(i)
		print "Day {day} {name}".format(day=i, name=d["name"])
		for c in d["specials"]:
			print "  ", c

if __name__ == "__main__":
	main()
