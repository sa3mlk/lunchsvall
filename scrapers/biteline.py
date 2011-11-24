#!/usr/bin/env python
# -*- encoding: utf8 -*-
from datetime import date

def get_daily_specials(day=None):

	daily_specials = {
		"name": u"Bite Line",
		"specials": [],
		"streetaddress": "Köpmangatan 20, Sundsvall",
		"dataurl": "http://www.biteline.nu/",
		"mapurl": "http://www.hitta.se/ViewDetailsPink.aspx?Vkiid=sVs3hH7uDE0WvL2C95PX9g%253d%253d"
	}

	if day == None:
		day = date.today().weekday()

	# No lunch on Saturday or Sunday
	if day == 5 or day == 6:
		return daily_specials

	specials = map(lambda x: "Pizza %d: %s" % (x[0] + 1, x[1]), enumerate([
		# Monday
		[u"Kebabkött, tomat, röd lök, fefferoni & kebabsås",
		 u"Skinka & ananas",
		 u"Tomat, jalapeños, ananas, svarta oliver & champinjoner"],
		# Tuesday
		[u"Vitlökskötbullar, jalapeños, ananas & paprika",
		 u"Skinka & champinjoner",
		 u"Tomat, paprika, svarta oliver & lök"],
		# Wednesday
		[u"Pepperonikorv, ananas, lök & pepparmix",
		 u"Skinka & ananas",
		 u"Tomat, svarta oliver, fetaost, lök & fefferoni"],
		# Thursday
		[u"Taconötfärs, salsa, ananas & lök",
		 u"Skinka, tomat & oregano",
		 u"Tomat, champinjoner, paprika & ananas"],
		# Friday
		[u"Pepperonikorv, vitlökskötbullar & fefferoni",
		 u"Skinka & champinjoner",
		 u"Ananas, paprika, lök & pepparmix"]
	][day]))

	daily_specials["specials"] = specials

	return daily_specials

def main():
	def print_specials(day, d):
		print "Day", day
		for c in d["specials"]:
			print "  ", c

	d = get_daily_specials(0)
	print d["name"]
	print_specials(0, d)
	for day in range(1, 5):
		print_specials(day, get_daily_specials(day))

if __name__ == "__main__":
	main()

