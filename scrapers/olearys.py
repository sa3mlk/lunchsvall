#!/usr/bin/env python
# -*- encoding: utf8 -*-

from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen
from datetime import date
import re

URL = "http://www.olearys.se/Default.aspx?CMSLanguageID=15&ArticleID=4815&UnitID=140"

def get_daily_specials(day=None):
	page = urlopen(URL)
	soup = BeautifulSoup(page)
	page.close()

	daily_specials = {
		"name": "O'learys",
		"specials": [],
		"streetaddress": "Storgatan 40, Sundsvall",
		"dataurl": URL,
		"mapurl": "http://www.hitta.se/ViewDetailsPink.aspx?Vkiid=haPYurZlRgoPvd8psQoRNA%253d%253d&Vkid=5736522"
	}

	if day == None:
		day = date.today().weekday()

	# No lunch on Saturday or Sunday
	if day == 5 or day == 6:
		return daily_specials

	style = "font-family: Tahoma, Verdana, Helvetica, Arial; ;font-size:11pt"
	menu = soup.find("span", {"style": style})
	days = menu.findAll("span")

	def split_specials(text):
		for i, c in enumerate(text[:-1]):
			c2 = text[i+1]
			if c.islower() and c2.isupper() and not c2.isspace():
				return map(lambda x: x.strip(), [text[0:i+1], text[i+1:]])

	daily_specials["specials"] = split_specials(days[day].text)

	return daily_specials

def main():
	for day in range(5):
		d = get_daily_specials(day)
		print "%s Day %d" % (d["name"], day)
		for c in d["specials"]:
			print "  ", c

if __name__ == "__main__":
	main()

