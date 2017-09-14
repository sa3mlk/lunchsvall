#!/usr/bin/env python
# -*- encoding: utf8 -*-

URL = "http://restaurangtraktoren.se/lunchmeny.html"

def get_daily_specials(day=None):
	from BeautifulSoup import BeautifulSoup
	from urllib2 import urlopen
	from datetime import date

	daily_specials = {
		"name": "Restaurang Traktören",
		"specials": [],
		"streetaddress": "Norra Vägen 30, Sundsvall",
		"dataurl": URL,
		"mapurl": "https://www.hitta.se/kartan/pl/Norra%20V%C3%A4gen%2030%20%20Sundsvall/"
	}

	page = urlopen(URL)
	soup = BeautifulSoup(page)
	page.close()

	weekday = date.today().weekday() if day is None else day

	# Only Monday - Friday
	if weekday > 4:
		return daily_specials

	days = [u"Måndag", u"Tisdag", u"Onsdag", u"Torsdag", u"Fredag", "Smaklig"]
	day = soup.find("p", text=days[weekday])

	parent = day.findParent("p")
	siblings = parent.findNextSiblings("p")
	specials = []

	for p in siblings:
		if days[weekday+1] in p.text:
			break
		specials.append(p.text)

	daily_specials["specials"] = filter(lambda x: len(x) > 6, specials)
	return daily_specials

def main():
	import test
	test.run(get_daily_specials)

if __name__ == "__main__":
	main()
