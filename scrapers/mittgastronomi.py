#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen
from datetime import date

URL = "http://mittgastronomi.nordicshops.com/category.html/"

def get_daily_specials(day=None):

	daily_specials = {
		"name": "Mitt Gastronomi",
		"specials": [],
		"streetaddress": "Storgatan 3, Sundsvall",
		"dataurl": URL,
		"mapurl": "http://www.hitta.se/mitt+gastronomi/sundsvall/y~dRCXU1Gq?vad=Mitt+Gastronomi%2C+Storgatan+Sundsvall"
	}

	if day == None:
		day = date.today().weekday()

	# Only Monday - Friday
	if day > 4:
		return daily_specials

	daily_specials["dataurl"] = daily_specials["dataurl"] + ["man", "tis", "ons", "tors", "fre"][day] + "dag"

	page = urlopen(daily_specials["dataurl"])
	soup = BeautifulSoup(page)
	page.close()
	day = [u"Måndag", u"Tisdag", u"Onsdag", u"Torsdag", u"Fredag"][day]

	containers = soup.findAll("div", {"class": "product-small-textcontainer"})
	for c in containers:
		daily_specials["specials"].extend([" ".join(c.find("div", {"class": "name"}).text.split()[3:])])

	return daily_specials

def main():
	import test
	test.run(get_daily_specials)

if __name__ == "__main__":
	main()

