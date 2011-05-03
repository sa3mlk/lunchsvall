#!/usr/bin/env python
# -*- encoding: utf8 -*-

# You won't be able to run this locally since it requires the JSON store
# for the Twitter-bot at http://twitter.com/#!/Delicerano

import simplejson as json
from datetime import date

JSON_STORE = "/home/jonasg/code/delicerano/daily_specials"

def get_daily_specials():
	d = date.today()
	daily_specials = {"name": u"Delicerano", "specials": []}

	# No lunch on Saturday or Sunday
	if d.weekday() == 5 or d.weekday() == 6:
		return daily_specials

	year, week = d.isocalendar()[:2]
	fn = "%s/%s-week%d.json" % (JSON_STORE, year, week)
	with file(fn) as f:
		weekly_menu = json.loads(f.read())
	day_key = d.strftime("%A").lower()

	daily_specials["specials"].append(weekly_menu["specials"][day_key])
	return daily_specials

def main():
	d = get_daily_specials()
	print d["name"].encode("UTF-8")
	for c in d["specials"]:
		print "  ", c.encode("UTF-8")

if __name__ == "__main__":
	main()

