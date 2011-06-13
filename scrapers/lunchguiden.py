#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen
from datetime import date

URL = "http://kampanjsajt.nu/st/lunchguiden/"

def get_daily_specials():
	page = urlopen(URL)
	soup = BeautifulSoup(page)
	page.close()

	restaurants = [(i.text, i["href"][1:]) for i in
		soup.find("div", id="menu").findChildren("a", {"class": "block"})]

	daily_specials = []

	# No lunch on Saturday or Sunday
	day = date.today().weekday()
	if day == 5 or day == 6:
		return daily_specials

	for r in restaurants:
		def get_details():
			# Return a list of all specials for the given restaurant by its link reference
			anchor = r[1]
			div = soup.find("a", {"class": "ref", "name": anchor})

			# Extract and strip the street address and map URL
			em = div.parent.find("em")
			street = str(em.contents[0]).strip().replace("\r\n", " ")
			mapurl = str(em.contents[1]["href"]).strip()

			ul = div.parent.find("ul")

			# Return an empty "specials" list if there are no daily specials available,
			# otherwise all <li> tags in the list.
			return {
				"specials": [li.text for li in ul] if ul else [],
				"streetaddress": street,
				"dataurl": "http://kampanjsajt.nu/st/lunchguiden/#" + anchor,
				"mapurl": mapurl
			}

		s = get_details()
		if len(s["specials"]):
			daily_specials.append({
				"name": r[0],
				"specials": s["specials"],
				"streetaddress": s["streetaddress"],
				"dataurl": s["dataurl"],
				"mapurl": s["mapurl"]
			})

	return daily_specials

def main():
	for d in get_daily_specials():
		print d["name"].encode("UTF-8")
		print "streetaddress:", d["streetaddress"]
		print "mapurl:", d["mapurl"]
		print "dataurl:", d["dataurl"]
		for c in d["specials"]:
			print "  ", c.encode("UTF-8")

if __name__ == "__main__":
	main()

