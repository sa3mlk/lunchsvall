#!/usr/bin/env python
# -*- encoding: utf8 -*-

# This scraper don't care about the day number / lazy me

URL = "https://eurest.mashie.eu/mashie/MashiePublic/MenuPresentation/Common/MenuSite.aspx?SiteId=bb7288de-fffd-44de-944d-a30300d114d3"

def get_daily_specials(day=None):
	from BeautifulSoup import BeautifulSoup
	from urllib2 import urlopen
	from datetime import date
	import re

	daily_specials = {
		"name": "Brandstation",
		"specials": [],
		"streetaddress": "Köpmangatan 29, Sundsvall",
		"dataurl": URL,
		"mapurl": "http://www.hitta.se/ViewDetailsPink.aspx?Vkiid=3LhMg0f89wskR4cV3PAzfA%253d%253d&Vkid=1622144"
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

