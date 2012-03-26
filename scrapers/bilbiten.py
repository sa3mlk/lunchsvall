#!/usr/bin/env python
# -*- encoding: utf8 -*-

from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen
from datetime import date

URL = "http://www.gidlund.dns2go.com/bilbiten/matsedel.asp"

def get_daily_specials(day=None):
	page = urlopen(URL)
	soup = BeautifulSoup(page)
	page.close()

	daily_specials = {
		"name": "Restaurang Bilbiten",
		"specials": [],
		"streetaddress": "Bultgatan 1, Sundsvall",
		"dataurl": URL,
		"mapurl": "http://www.hitta.se/restaurang+bilbiten/sundsvall/xjZwUJaaB6"
	}

	if day == None:
		day = date.today().weekday()

	# No lunch on Saturday or Sunday
	if day == 5 or day == 6:
		return daily_specials

	table = soup.findAll("table", id="table1")[1:][day]
	daily_specials["specials"] = [tr.text.strip().replace("&nbsp;", "") for tr in table.findAll("tr")]

	return daily_specials

def main():
	for day in range(5):
		d = get_daily_specials(day)
		print "%s Day %d" % (d["name"], day)
		for c in d["specials"]:
			print "  ", c

if __name__ == "__main__":
	main()

