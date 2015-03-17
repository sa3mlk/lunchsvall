#!/usr/bin/env python
# -*- encoding: utf-8 -*-

URL = "http://bryners.se"

def get_daily_specials(day=None):
	from BeautifulSoup import BeautifulSoup
	from urllib2 import urlopen
	from datetime import date

	daily_specials = {
		"name": "Bryners",
		"specials": [],
		"streetaddress": "Kyrkogatan 24, Sundsvall",
		"dataurl": URL,
		"mapurl": "http://www.hitta.se/ViewDetailsPink.aspx?Vkiid=ims%2bc70lKiXCPdGPetps6w%253d%253d"
	}

	if day == None:
		day = date.today().weekday()

	page = urlopen(URL)
	soup = BeautifulSoup(page)
	page.close()

	try:
		day = [u"Måndag", u"Tisdag", u"Onsdag", u"Torsdag", u"Fredag"][day]
		anchor = soup.find(lambda tag: tag.name == "span" and tag.text[0:len(day)] == day)
		daily_specials["specials"] = [li.text for li in anchor.parent.findNextSibling("ul")]
	except IndexError:
		pass

	return daily_specials

def main():
	import test
	test.run(get_daily_specials)

if __name__ == "__main__":
	main()
