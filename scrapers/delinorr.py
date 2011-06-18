#!/usr/bin/env python
# -*- encoding: utf8 -*-

from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen
import re
from datetime import date

URL = "http://www.delinorr.se/filearea_15.html"

def get_weekly(soup, match):
	# First locate the <span> according to the match argument
	pattern = re.compile("^" + match, re.IGNORECASE)
	span = soup.find(lambda tag: tag.name == "span" and pattern.match(tag.text))
	# Next we need the parent <p> from the <span>
	p = span.findParent("p")
	# And the first sibling <table>
	table = p.findNextSiblings("table", {"class": "MsoNormalTable", "cellpadding": "0", "border": "0"})[0]
	# Last thing is the first <td> from the second <tr> 
	return table.findAll("tr", limit=2)[1].td.text

def get_daily_specials(day=None):
	page = urlopen(URL)
	soup = BeautifulSoup(page)
	page.close()

	daily_specials = {
		"name": "Deli Norr",
		"specials": [],
		"streetaddress": "Nybrogatan 5, Sundsvall",
		"dataurl": URL,
		"mapurl": "http://www.hitta.se/ViewDetailsPink.aspx?Vkiid=tURKyBsIBejyvRtSYTRetQ%253d%253d"
	}

	if day == None:
		day = date.today().weekday()

	# Only Monday - Friday
	if day > 4:
		return daily_specials

	day = [u"m&aring;ndag", u"tisdag", u"onsdag", u"torsdag", u"fredag"][day]
	pattern = re.compile("^" + day, re.IGNORECASE)
	today = soup.find(lambda tag: tag.name == "span" and pattern.match(tag.text)) 
	parent = today.findParent("tr")
	day = parent.findNextSiblings("tr", limit=1)[0]

	daily_special = day.findChild("td").text
	daily_specials["specials"].append(daily_special)
	daily_specials["specials"].append("Veckans soppa: " + get_weekly(soup, "Veckans soppa"))
	daily_specials["specials"].append("Veckans GI: " + get_weekly(soup, "Veckans&nbsp;GI"))

	return daily_specials

def main():
	d = get_daily_specials()
	print d["name"]
	for day in range(5):
		d = get_daily_specials(day)
		print "Day", day
		if len(d["specials"]) == 0:
			continue
		else:
			for c in d["specials"]:
				print " ", c

if __name__ == "__main__":
	main()
