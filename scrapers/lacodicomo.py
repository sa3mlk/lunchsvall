#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from bs4 import BeautifulSoup, NavigableString, Tag
from urllib.request import urlopen
from datetime import date
import re

URL = "http://laco.se/lunch/"

def get_daily_specials(day=None):
	page = urlopen(URL)
	soup = BeautifulSoup(page)
	page.close()

	daily_specials = {
		"name": "Laco di Como",
		"specials": [],
		"streetaddress": "Timmervägen 6, Sundsvall",
		"dataurl": URL,
		"mapurl": "http://www.hitta.se/ViewDetailsPink.aspx?Vkiid=VgwibzXcvb%252fAf1XfiCvetg%253d%253d"
	}

	if day == None:
		day = date.today().weekday()

	# Only Monday - Friday
	if day > 4:
		return daily_specials

	day = [u"Måndag", u"Tisdag", u"Onsdag", u"Torsdag", u"Fredag"][day]
	pattern = re.compile(day, re.IGNORECASE)

	anchor = soup.find(lambda tag: tag.name == "h2" and tag.text == day)
	if not anchor:
		return daily_specials

	while True:
		anchor = anchor.next
		if isinstance(anchor, Tag):
			if anchor.name == "h2":
				break 
			else:
				daily_specials["specials"].append(anchor.text.strip())
		if len(daily_specials["specials"]) > 5:
			break

	return daily_specials

def main():
	def print_specials(day, d):
		print(" Day", day)
		for c in d["specials"]:
			print("  ", c)
		print("")

	for day in range(0, 5):
		print_specials(day, get_daily_specials(day))

if __name__ == "__main__":
	main()

