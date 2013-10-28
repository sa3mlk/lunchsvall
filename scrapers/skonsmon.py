#!/usr/bin/env python
# -*- encoding: utf8 -*-

from urllib2 import urlopen
from datetime import date
import simplejson as json

URL = "http://www.gulle.se/skonsmon/data/current.json"

def get_daily_specials(day=None):
	page = urlopen(URL)
	data = json.loads(page.read())
	page.close()

	daily_specials = {
		"name": "Restaurang Skönsmon",
		"specials": [],
		"streetaddress": "Fridhemsgataj 74, Sundsvall",
		"dataurl": "https://www.facebook.com/pages/Restaurang-Skönsmon/290777847709062",
		"mapurl": "http://www.hitta.se/fikret+aypek/sundsvall/hgjC5OHGbk"
	}

	if day == None:
		day = date.today().weekday()

	# Only Monday - Friday
	if day > 4:
		return daily_specials

	d = ["mon", "tue", "wed", "thu", "fri"][day]
	keys = ["%s%d" % (d, i) for i in range(1, 4)]
	daily_specials["specials"] = filter(len, [data[k] for k in keys])

	return daily_specials

def main():
	for day in range(5):
		d = get_daily_specials(day)
		if len(d["specials"]) == 0:
			continue
		print "%s | day %d" % (d["name"], day)
		for c in d["specials"]:
			print "  ", c

if __name__ == "__main__":
	main()

