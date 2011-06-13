#!/usr/bin/env python
# -*- encoding: utf8 -*-

from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen
from datetime import date
import re

URL = "http://metropol.norrvidden.se/lunch.php"

def get_daily_specials(day=None):
	page = urlopen(URL)
	soup = BeautifulSoup(page)
	page.close()

	daily_specials = {
		"name": "Metropol Restaurang & Café",
		"specials": [],
		"streetaddress": "Universitetsallén 32, Sundsvall",
		"dataurl": URL,
		"mapurl": "http://www.hitta.se/ViewDetailsPink.aspx?Vkiid=2tPymsbRskRGTMh%2b%252fy0IEw%253d%253d"
	}

	if day == None:
		day = date.today().weekday()

	# No lunch on Saturday or Sunday
	if day == 5 or day == 6:
		return daily_specials

	lunch_menu = soup.find("div", {"id": "conference_text", "class": "lunch_menu"})
	day = [u"Måndag", u"Tisdag", u"Onsdag", u"Torsdag", u"Fredag"][day]

	pattern = re.compile("^" + day)
	today = soup.find(lambda tag: tag.name == "li" and pattern.match(tag.text))
	stripped = today.text[len(day):].strip().replace(u"- ", u"─ ")
	daily_specials["specials"] = filter(lambda x: len(x) > 0, stripped.split("-"))

	return daily_specials

def main():
	for day in range(5):
		d = get_daily_specials(day)
		print d["name"]
		for c in d["specials"]:
			print "  ", c

if __name__ == "__main__":
	main()

