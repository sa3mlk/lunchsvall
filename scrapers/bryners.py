#!/usr/bin/env python
# -*- encoding: utf-8 -*-

def get_daily_specials(day=None):
	from BeautifulSoup import BeautifulSoup
	from urllib2 import urlopen
	from datetime import date

	daily_specials = [
		{
			"name": "Bryners Kök",
			"specials": [],
			"streetaddress": "Kyrkogatan 24, Sundsvall",
			"dataurl": "http://bryners.se/bryners.se.html",
			"mapurl": "http://www.hitta.se/ViewDetailsPink.aspx?Vkiid=ims%2bc70lKiXCPdGPetps6w%253d%253d"
		},
		{
			"name": "Bryners Bistro",
			"specials": [],
			"streetaddress": "Strandgatan 10, Sundsvall",
			"dataurl": "http://bryners.se/bryners%20bistro.html",
			"mapurl": "http://www.hitta.se/strand+restauran+och+bar/sundsvall/iyyL~xPP2Z?vad=adress%3AStrandgatan+10+Sundsvall"
		}
	]

	if day == None:
		day = date.today().weekday()
	day = [u"Måndag", u"Tisdag", u"Onsdag", u"Torsdag", u"Fredag", u"Lördag", u"Söndag"][day]

	for d in daily_specials:
		page = urlopen(d["dataurl"])
		soup = BeautifulSoup(page)
		page.close()

		try:
			anchor = soup.find(lambda tag: tag.name == "span" and tag.text[0:len(day)] == day)
			d["specials"] = [li.text for li in anchor.parent.findNextSibling("ul")] if anchor else []
		except IndexError:
			pass

	return daily_specials

def main():
	import test
	test.run(get_daily_specials)

if __name__ == "__main__":
	main()
