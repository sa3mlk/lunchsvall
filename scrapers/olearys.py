#!/usr/bin/env python
# -*- encoding: utf8 -*-

from BeautifulSoup import BeautifulSoup, Tag, NavigableString
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

	# Some weeks there are one <span> for each day in the week, but other weeks
	# they use the same <span> for all weekdays.

	if days:
		# They have separate <span>'s for each day
		def split_specials(text):
			for i, c in enumerate(text[:-1]):
				c2 = text[i+1]
				if c.islower() and c2.isupper() and not c2.isspace():
					return map(lambda x: x.strip(), [text[0:i+1], text[i+1:]])

		daily_specials["specials"] = split_specials(days[day].text)
	else:
		# All days are problably in the same <span>
		days = filter(lambda x: len(x.text) > 1 if isinstance(x, Tag) else len(x) > 1, menu.contents)
		days = map(lambda y: unicode(y).strip() if isinstance(y, NavigableString) else y.text.strip(), days)
		swe_days = [u"Måndag", u"Tisdag", u"Onsdag", u"Torsdag", u"Fredag"]
		day = swe_days[day]
		for i, c in enumerate(days):
			if c == day:
				# Allow three daily specials
				for j in range(1, 4):
					try:
						if days[i+j] in swe_days:
							return daily_specials
						else:
							daily_specials["specials"].append(days[i+j])
					except IndexError:
						return daily_specials

	return daily_specials

def main():
	for day in range(5):
		d = get_daily_specials(day)
		print "%s Day %d" % (d["name"], day)
		for c in d["specials"]:
			print "  ", c

if __name__ == "__main__":
	main()

