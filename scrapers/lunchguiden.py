#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen
from datetime import date

BLACKLIST = [
	u"Laco di Como",
	u"Restaurang Brandstation",
	u"Restaurang Metropol"
]
URL = "http://wp.mittmedia.se/lunchguiden/st/"

def get_daily_specials():
	page = urlopen(URL)
	soup = BeautifulSoup(page)
	page.close()

	restaurants = [(i.text, i["onclick"].split("'")[1]) for i in
		soup.find("div", id="menu").findChildren("a", {"class": "block"})]

	daily_specials = []

	# No lunch on Saturday or Sunday
	day = date.today().weekday()
	if day == 5 or day == 6:
		return daily_specials

	# Filter out unwanted restaurants since we have unique scrapers for them
	restaurants = filter(lambda r: r[0] not in BLACKLIST, restaurants)

	for r in restaurants:
		def get_details():
			# Return a list of all specials for the given restaurant by its link reference
			anchor = r[1]
			div = soup.find("div", id=r[1])

			href = div.parent.find("p").findChild("a")
			mapurl = href["href"] if href else ""

			# Extract and strip the street address
			em = div.parent.find("em")

			street = str(em.contents[0]).strip().replace("\r\n", " ")
			#mapurl = unicode(em.contents[1]["href"]).strip()

			ul = div.parent.find("ul")

			# Return an empty "specials" list if there are no daily specials available,
			# otherwise all <li> tags in the list.
			return {
				"specials": [li.text for li in ul] if ul else [],
				"streetaddress": street,
				"dataurl": URL + "#" + anchor,
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
		raw_input()

if __name__ == "__main__":
	main()

