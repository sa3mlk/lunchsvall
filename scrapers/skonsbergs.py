#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from urllib.request import urlopen
from datetime import date
try:
	import simplejson as json
except ImportError:
	import json

URL = "http://www.gulle.se/~jonasg/skonsbergs/data/current.json"
MAPURL = "https://www.hitta.se/folkets+hus+skönsberg/sundsvall/i~xMjw---X"

def get_daily_specials(day=None):
	page = urlopen(URL)
	data = json.loads(page.read())
	page.close()

	daily_specials = {
		"name": u"Restaurang Bibliotequet",
		"specials": [],
		"streetaddress": "Medborgargatan 35, Sundsvall",
		"dataurl": "http://eqhouse.se",
		"mapurl": MAPURL
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
		print("%s | day %d" % (d["name"], day))
		for c in d["specials"]:
			print("  ", c)

if __name__ == "__main__":
	main()

