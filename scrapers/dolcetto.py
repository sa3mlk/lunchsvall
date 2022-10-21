#!/usr/bin/env python
# -*- encoding: utf8 -*-

from bs4 import BeautifulSoup, NavigableString
from urllib.request import urlopen
from datetime import date

URL = "http://www.dolcetto.nu/lunch"

def get_daily_specials(day=None):
	page = urlopen(URL)
	soup = BeautifulSoup(page)
	page.close()

	daily_specials = {
		"name": "Dolcetto",
		"specials": [],
		"streetaddress": "Kyrkogatan 8, Sundsvall",
		"dataurl": URL,
		"mapurl": "http://www.hitta.se/ViewDetailsPink.aspx?Vkiid=4uG7%252fiYMOcHQKtp0VSkMNw%253d%253d&Vkid=3215131"
	}

	if day == None:
		day = date.today().weekday()

	# No lunch on Saturday or Sunday
	if day == 5 or day == 6:
		return daily_specials

	day = [u"måndag", u"tisdag", u"onsdag", u"torsdag", u"fredag"][day]
	anchor = soup.find(lambda t: t.name == "h2" and t.text == "Lunchmeny")
	menu = filter(lambda x: isinstance(x, NavigableString), anchor.findNextSibling("p"))
	for i, v in enumerate(menu):
		if day == v.lower():
			daily_specials["specials"].append(menu[i+1])
			break	

	return daily_specials

def main():
	for day in range(5):
		d = get_daily_specials(day)
		print("%s Day %d" % (d["name"], day))
		for c in d["specials"]:
			print("  ", c)

if __name__ == "__main__":
	main()

