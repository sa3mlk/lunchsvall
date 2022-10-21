#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import date
import re

URL = "http://skonerten.se/meny/"

def get_daily_specials(day=None):
	page = urlopen(URL)
	soup = BeautifulSoup(page)
	page.close()

	daily_specials = {
		"name": "Skonerten",
		"specials": [],
		"streetaddress": "Packhusgatan 4, Sundsvall",
		"dataurl": URL,
		"mapurl": "http://www.hitta.se/ViewDetailsPink.aspx?Vkiid=11IAWjLqMBv1aPZn4Dip9g%253d%253d&Vkid=1456953"
	}

	if day == None:
		day = date.today().weekday()

	# Only Monday - Friday
	if day > 4:
		return daily_specials

	day = [u"Måndag:", u"Tisdag:", u"Onsdag:", u"Torsdag:", u"Fredag:"][day]

	span = soup.find(lambda tag: tag.name == "span" and tag.text == day)

	parent = span.findParent("h6")
	daily_specials["specials"].append(parent.text[len(day):].strip())
	daily_specials["specials"].extend([t.text.strip() for t in parent.findNextSiblings("h6", limit=2)])

	return daily_specials

def main():
	for day in range(5):
		d = get_daily_specials(day)
		print("%s Day %d" % (d["name"], day))
		for c in d["specials"]:
			print("  ", c)

if __name__ == "__main__":
	main()

