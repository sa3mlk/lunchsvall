#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from bs4 import BeautifulSoup, NavigableString
from urllib.request import urlopen
from datetime import date

URL = "https://docs.google.com/document/d/14j7TgcekgZ0hB90KXwOY35cHsfUIf-odPndVDdcspvE/pub?embedded=true"

def get_daily_specials(day=None):
	page = urlopen(URL)
	soup = BeautifulSoup(page)
	page.close()

	daily_specials = {
		"name": "Opus Restaurang & Pianobar",
		"specials": [],
		"streetaddress": "Storgatan 12, Sundsvall",
		# NB: Different URL for link.
		"dataurl": "http://www.opuspianobar.se/opus-mat.html#lunch",
		"mapurl": "https://www.hitta.se/opus+restaurang+och+pianobar/sundsvall/dMsvvOJJK7?vad=Opus+Restaurang+%26+Pianobar%2C+Storgatan+Sundsvall"
	}

	day = date.today().weekday() if day is None else day

	# Only Monday - Friday
	if day > 4:
		return daily_specials

	days = [u"M&aring;ndag:", u"Tisdag:", u"Onsdag:", u"Torsdag:", u"Fredag:", u"L&oring;rdag:"]
	today = days[day]
	tomorrow = days[day+1]

	anchor = soup.find("p", text=today).findParent("p")
	for p in [t.text for t in anchor.findNextSiblings("p")]:
		if tomorrow in p:
			break
		daily_specials["specials"].append(p)

	return daily_specials

def main():
	import test
	test.run(get_daily_specials)

if __name__ == "__main__":
	main()

