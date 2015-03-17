#!/usr/bin/env python
# -*- encoding: utf-8 -*-

URL = "http://eurest.mashie.se/mashie/MashiePublic/MenuPresentation/Common/MenuSite.aspx?SiteId=b3420841-fc1a-410b-8bbe-a2ff00b518e2"

def get_daily_specials(day=None):
	from BeautifulSoup import BeautifulSoup
	from urllib2 import urlopen
	from datetime import date
	import re

	daily_specials = {
		"name": "Restaurang Nöjet",
		"specials": [],
		"streetaddress": "Sundsvalls Sjukhus, Lasarettsvägen",
		"dataurl": URL,
		"mapurl": "http://www.hitta.se/sundsvalls+sjukhus/sundsvall/LzggZC-vvm?vad=sundsvalls+sjukhus"
	}

	page = urlopen(URL)
	soup = BeautifulSoup(page)
	page.close()

	div = soup.find("div", {"class": re.compile("Menu_Today")})
	div = div.findParent("div", {"class": "Menu_DayHeader"})
	div = div.findNextSibling("div", style="width:385px")

	daily_specials["specials"] = map(lambda x: x.strip(),
		[t.find("span", {"class": "Menu_DayMealName"}).text for t in div.findAll("table")]
	)

	return daily_specials

def main():
	import test
	test.run(get_daily_specials)

if __name__ == "__main__":
	main()

