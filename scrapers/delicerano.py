#!/usr/bin/env python
# -*- encoding: utf8 -*-

from urllib.request import urlopen
from datetime import date
import simplejson as json

URL = "http://www.gulle.se/delicerano/data/current.json"

def get_daily_specials(day=None):
	page = urlopen(URL)
	data = json.loads(page.read())
	page.close()

	daily_specials = {
		"name": "Delicerano",
		"specials": [],
		"streetaddress": "Sjögatan 7, Sundsvall",
		"dataurl": "http://delicerano.se/Ny-sida-2.htm",
		"mapurl": "http://www.hitta.se/ViewDetailsPink.aspx?Vkiid=BjgBy%2bYy%252fc3YvyHSBs8Xeg%253d%253d&Vkid=2856959"
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

