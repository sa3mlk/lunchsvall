#!/usr/bin/env python
from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen
from datetime import date

URL = "http://2.st.nu/nyastnu/polopoly/iframes/lunchguiden.php"

# TODO: Add more restaurants:
#	* Delicerano
#   * Bryners
#   * Brandstation
#   * etc.

def get_daily_specials(restaurant_url):
	page = urlopen(URL + restaurant_url)
	soup = BeautifulSoup(page)
	restaurant_name = soup.find("h1").text

	swe_days = { 1: "M&aring;ndag",	2: "Tisdag", 3: "Onsdag", 4: "Torsdag", 5: "Fredag" }
	swe_months = { 1: "januari", 2: "februari", 3: "mars", 4: "april", 5: "maj", 6: "juni",
		7: "juli", 8: "augusti", 9: "september", 10: "oktober", 11: "november", 12: "december" }

	daily_specials = {"name": restaurant_name, "specials": []}

	try:
		d = date.today()
		match = "%s %d %s" % (swe_days[d.isoweekday()], d.day, swe_months[d.month])
	except KeyError:
		return daily_specials

	# col482 is the column with all days
	column = soup.find("div", id="col482")
	pads = column.findAll("div", { "class": "pad" })
	specials = []
	for pad in pads:
		font = pad.find("font")
		if font is not None and font.text == match:
			specials = [li.text for li in pad.findAll("li")]

	daily_specials["specials"] = join_specials(specials)
	return daily_specials

# Join lines starting with a lower case character since many subscribers
# use several <li> items to describe one daily special.
def join_specials(v):
	nv = []
	for c in v:
		if nv and c[0].islower():
			nv[-1] += " " + c
		else:
			nv.append(c)
	return nv

def parse_lunchguide():
	daily_specials = []

	#TODO: Check that we get a "File not found" error
	page = urlopen(URL)
	soup = BeautifulSoup(page)

	# Find all divs with id="lunchbox"
	divs = soup.findAll("div", id="lunchbox")

	# For each href in the lunchbox: Follow the link and scrape all the daily specials.
	daily_specials = [get_daily_specials(div.find("a")["href"]) for div in divs]

	return daily_specials

def main():
	daily_specials = parse_lunchguide()
	for d in daily_specials:
		print d["name"].encode("UTF-8")
		for c in d["specials"]:
			print "  ", c.encode("UTF-8")

if __name__ == "__main__":
	main()

