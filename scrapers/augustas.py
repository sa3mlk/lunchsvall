#!/usr/bin/env python
# -*- encoding: utf8 -*-
import re

from bs4 import BeautifulSoup, NavigableString
from urllib.request import urlopen
from datetime import date

URL = "http://www.baltichotell.com/lunch.aspx"

def get_daily_specials(day=None):
	page = urlopen(URL)
	data = page.read()
	page.close()
	data = data.replace(b'\r\n', b' ')
	data = data.replace(b'\n', b' ')
	data = data.replace(b'\r', b' ')
	soup = BeautifulSoup(data)

	daily_specials = {
		"name": "Augustas Kök",
		"specials": [],
		"streetaddress": "Sjögatan 5, Sundsvall",
		"dataurl": URL,
		"mapurl": "https://www.hitta.se/best+western+hotel+baltic/sundsvall/hglwn1bJJA"
	}

	if day == None:
		day = date.today().weekday()

	# No lunch on Saturday or Sunday
	if day == 5 or day == 6:
		return daily_specials

	days = ["Måndag", "Tisdag", "Onsdag", "Torsdag", "Fredag"]
	wday = days[day]

	for br in soup.find_all('br'):
		br.replace_with('\n')

	text = soup.text

	def findSpecial(name):
		pattern = r"^\s*%s:?\s*\n(.*)$" % name
		m = re.search(pattern, text, re.MULTILINE | re.IGNORECASE)
		return re.sub(r'\s+', ' ', m.group(1))

	specials = [
		("Dagens", wday),
		("Fisk", "Veckans Fisk"),
		("Gryta", "Veckans gryta"),
		("Vegetarisk", "Veckans vegetariska"),
		("Sallad", "Veckans sallad")
	]

	for t, s in specials:
		try:
			daily_specials["specials"].append(t + ": " + findSpecial(s))
		except AttributeError:
			pass

	return daily_specials

def main():
	import test
	test.run(get_daily_specials)

if __name__ == "__main__":
	main()
