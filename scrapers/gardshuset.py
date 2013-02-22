#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from urllib2 import urlopen
from datetime import date
try:
	import simplejson as json
except ImportError:
	import json

URL = "http://www.gulle.se/gardshuset/data/current.json"

def get_daily_specials(day=None):
	page = urlopen(URL)
	data = json.loads(page.read())
	page.close()

	daily_specials = {
		"name": u"Restaurang Gårdshuset",
		"specials": [],
		"streetaddress": "Arthur Engbergs Väg 11, Sundsvall",
		"dataurl": "http://www.sidsjohotell.se/restaurang-gardshuset/",
		"mapurl": "http://www.hitta.se/ViewDetailsPink.aspx?Vkiid=ww6BfFoSzg9YJaefKRj2tQ%253d%253d&Vkid=2670064"
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

