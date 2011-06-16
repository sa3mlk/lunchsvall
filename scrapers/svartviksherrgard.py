#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from BeautifulSoup import BeautifulSoup, NavigableString
from urllib2 import urlopen
from datetime import date
import re

URL = "http://www.svartviksherrgard.com/lunchbuffe/"

def get_daily_specials(day=None):
	page = urlopen(URL)
	soup = BeautifulSoup(page)
	page.close()

	daily_specials = {
		"name": "Svartviks Herrgård",
		"specials": [],
		"streetaddress": "Svartviksvägen 22, Kvissleby",
		"dataurl": URL,
		"mapurl": "http://www.hitta.se/ViewDetailsPink.aspx?Vkiid=pQwESnjorTiIAW4OJ3dOrg%253d%253d"
	}

	if day == None:
		day = date.today().weekday()

	days = [u"M&aring;ndag", u"Tisdag", u"Onsdag", u"Torsdag", u"Fredag", u"L&ouml;rdag", u"S&ouml;ndag"]
	day = days[day]

	pattern = re.compile(day)
	strong = soup.find("strong", text=day)
	parent = strong.findParent("p")
	siblings = parent.findNextSiblings("p", limit=10)
	for sibling in siblings:
		if sibling.text in days:
			break
		else:
			s = sibling.text.strip()
			s = s.replace("&nbsp;", "")
			if len(s):
				daily_specials["specials"].append(s)

	return daily_specials

def main():
	def print_specials(day, d):
		print " Day", day
		for c in d["specials"]:
			print "  ", c
		print ""

	d = get_daily_specials(0)
	print d["name"]
	print_specials(0, d)
	for day in range(1, 7):
		print_specials(day, get_daily_specials(day))

if __name__ == "__main__":
	main()

