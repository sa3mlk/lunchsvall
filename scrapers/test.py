#!/usr/bin/env python
# -*- encoding: utf8 -*-

def print_daily(d, day):
	daynames = { 0: "Måndag", 1: "Tisdag", 2: "Onsdag",
		3: "Torsdag", 4: "Fredag", 5: "Lördag", 6: "Söndag"
	}

	print "%s: %s" % (d["name"], daynames[day])
	if len(d["specials"]) == 0:
		print "   Ingen lunch"
	else:
		for c in d["specials"]:
			print "  ", c

def run(fn):
	from sys import argv
	if len(argv) == 2:
		# Print selected day
		day = int(argv[1])
		dailys = fn(day)
		if isinstance(dailys, list):
			for d in dailys:
				print_daily(d, day)
		else:
			print_daily(dailys, day)
	else:
		# Print all days
		for day in range(7):
			dailys = fn(day)
			if isinstance(dailys, list):
				for d in dailys:
					print_daily(d, day)
			else:
				d = fn(day)
				print_daily(d, day)

