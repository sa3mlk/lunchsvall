#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from bs4 import BeautifulSoup, NavigableString
from urllib.request import urlopen
from datetime import date

URL = "http://himlabadet.se/default.aspx?id=2115"

def get_daily_specials(day=None):
	page = urlopen(URL)
	soup = BeautifulSoup(page)
	page.close()

	daily_specials = {
		"name": "Himlabadet",
		"specials": [],
		"streetaddress": "Universitetsallén 13, Sundsvall",
		"dataurl": URL,
		"mapurl": "http://www.hitta.se/himlabadets+restaurang+och+café/sundsvall/xjj5UGKKeu"
	}

	if day == None:
		day = date.today().weekday()

	# Only Monday - Friday
	if day > 4:
		return daily_specials

	day = [u"Måndag", u"Tisdag", u"Onsdag", u"Torsdag", u"Fredag"][day]
	anchor = soup.find(lambda tag: tag.name == "strong" and tag.text == day)
	specials = filter(lambda t: isinstance(t, NavigableString), anchor.findParent().findNextSibling("p").contents)
	daily_specials["specials"] = filter(len, [s.replace("\n", "").strip() for s in specials])

	return daily_specials

def main():
	import test
	test.run(get_daily_specials)

if __name__ == "__main__":
	main()

