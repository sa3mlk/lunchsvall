#!/usr/bin/env python
# -*- encoding: utf8 -*-

from urllib.request import urlopen
import simplejson as json
from datetime import date
import re

URL = "https://graph.facebook.com/356782331040548/feed?access_token=AAACEdEose0cBAFT8bTma8aZCfsfFDAqxmCnZBIByp5m3ZAmIvRAt4NtzZBfv0cZAvYr1K5hfOm30UROw4xaecH9dHSO0uLjxjUMeeLbg1HQZDZD"

def get_daily_specials(day=None):
	page = urlopen(URL)
	data = json.loads(page.read())
	page.close()

	name = "Sundsvall Curryhouse"
	daily_specials = {
		"name": name,
		"specials": [],
		"streetaddress": "Köpmangatan 34, Sundsvall",
		"dataurl": URL,
		"mapurl": "http://www.hitta.se/karta?ref=start#var=k%C3%B6pmangatan%2034%2C%20sundsvall&sm=6&center=1577560:6920587&type=map&zl=9&bounds=6920432:1577304,6920743:1577816&rlm=1",
	}

	today = date.today().isoformat()
	for entry in data["data"]:
		if "status" == entry["type"] and entry.has_key("message"):
			if today in entry["created_time"]:
				for line in entry["message"].splitlines():
					# Filter out all "%d. " rows in the status update.
					mo = re.match("\d\. ", line)
					if mo:
						daily_specials["specials"].append(line[len(mo.group(0)):])

	return daily_specials

def main():
	d = get_daily_specials()
	print(d["name"])
	for c in d["specials"]:
		print(" ", c)

if __name__ == "__main__":
	main()

