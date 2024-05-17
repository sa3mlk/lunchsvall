#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import date
import json

URL = "http://lunchguide.nu/?page=sundsvall"

def get_daily_specials(day=None):
	if day == None:
		# No lunch on Saturday or Sunday
		day = date.today().weekday()
		if day == 5 or day == 6:
			return []

	page = urlopen(URL)
	soup = BeautifulSoup(page)
	page.close()

	def get_json():
		scripts = filter(len, [s.text for s in soup.findAll("script")])
		for s in scripts:
			start = s.find("var restaurants = ")
			if start < 0:
				continue
			start += 18
			s = s[start:]
			stop = s.find("}}];");
			return json.loads(s[:stop+3])

	def transform_json(obj):
		index = [u"Måndag", u"Tisdag", u"Onsdag", u"Torsdag", u"Fredag"][day]
		return {
			"name": obj["name"],
			"specials": list(filter(len, obj["food"][index].replace("<p>", "",).split("</p>"))),
			"streetaddress": obj["city"],
			"dataurl": "https://lunchguide.nu/?page={id}".format(**obj),
			"mapurl": "http://maps.google.com/maps?z=17&t=m&q=loc:{lat}+{long}".format(**obj)
		}

	return [transform_json(obj) for obj in get_json()]

def main():
	for day in range(5):
		for d in get_daily_specials(day):
			print(d["name"].encode("UTF-8"))
			print("streetaddress:", d["streetaddress"])
			print("mapurl:", d["mapurl"])
			print("dataurl:", d["dataurl"])
			for c in d["specials"]:
				print("  ", c.encode("UTF-8"))

if __name__ == "__main__":
	main()

