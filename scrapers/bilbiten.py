#!/usr/bin/env python
# -*- encoding: utf8 -*-

from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import date

#URL = "http://www.gidlund.dns2go.com/bilbiten/matsedel.asp"
URL = "http://www.bilbiten.eu/?page_id=50"

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

	text = soup.find("text", id=["man", "tis", "ons", "tor", "fre"][day])
	daily_specials["specials"] = text.renderContents().split("<br />")

	return daily_specials

def main():
	import test
	test.run(get_daily_specials)

if __name__ == "__main__":
	main()
