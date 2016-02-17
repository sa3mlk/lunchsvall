#!/usr/bin/env python
# -*- encoding: utf8 -*-

from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen
from datetime import date
import re

def scrape_wretmans(url, day=None):
	page = urlopen(url)
	soup = BeautifulSoup(page)
	page.close()

	if day == None:
		day = date.today().weekday()

	# No lunch on Saturday or Sunday
	if day == 5 or day == 6:
		return daily_specials

	# Modify all the strange <span class="SpellE"> and insert a space before the text
	for s in soup.findAll("span", {"class": "SpellE"}):
		soup.find(text=s.text).replaceWith("&nbsp;" + s.text)

	day = [u"Måndag", u"Tisdag", u"Onsdag", u"Torsdag", u"Fredag"][day]
	anchor = soup.find(lambda tag: tag.name == "p" and re.match(tag.text, day))
	siblings = anchor.findNextSiblings("p", limit=2)
	specials = []
	for i, s in enumerate([s.text for s in siblings]):
		s = re.sub("\n", " ", s)
		if s[0:6] == "&nbsp;":
			specials.append(s[6:])
		else:
			specials.append(s)

	return filter(len, specials)

def get_daily_specials(day=None):
	urls = [
		"http://wretmans.se/Lunchmenyer/Lunchmeny.htm",
		"http://www.wretmans.se/Lunchmenyer/Lunchmeny%20city.htm",
		"http://www.wretmans.se/Lunchmenyer/Lunchmeny%20mokajen.htm"
	]

	daily_specials = [
		{
			"name": "Wretmans",
			"specials": scrape_wretmans(urls[0], day),
			"streetaddress": "Murarvägen 8, Sundsvall",
			"dataurl": urls[0],
			"mapurl": "http://www.hitta.se/ViewDetailsPink.aspx?Vkiid=hvjaJ0xiNoaD1S2mBsxIoA%253d%253d"
		},
		{
			"name": "Wretmans City",
			"specials": scrape_wretmans(urls[1], day),
			"streetaddress": "Thulegatan 6, Sundsvall",
			"dataurl": urls[1],
			"mapurl": "http://www.hitta.se/wretmans+caf%C3%A9/sundsvall/hzWRPCw5X4"
		},
		{
			"name": "Wretmans Mokajen",
			"specials": scrape_wretmans(urls[2], day),
			"streetaddress": "Kolvägen 9, Sundsvall",
			"dataurl": urls[2],
			"mapurl": "http://www.hitta.se/s%C3%B6k?vad=Kolv%C3%A4gen%209%2C%20Sundsvall"
		}
	]

	return daily_specials

def main():
	for day in range(5):
		for r in get_daily_specials(day):
			print "%s Day %d" % (r["name"], day)
			for c in r["specials"]:
				print "  ", c
		print "-"*40

if __name__ == "__main__":
	main()

