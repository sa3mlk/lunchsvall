#!/usr/bin/env python
# -*- encoding: utf8 -*-

def print_daily(d, day):
	daynames = { 0: "Måndag", 1: "Tisdag", 2: "Onsdag",
		3: "Torsdag", 4: "Fredag", 5: "Lördag", 6: "Söndag"
	}

	print "%s: %s" % (d["name"], daynames[day])
	if len(d["specials"]) == 0:
		print "Ingen lunch"
	else:
		for c in d["specials"]:
			print "  ", c

def run(fn):
	from sys import argv
	if len(argv) == 2:
		# Print selected day
		day = int(argv[1])
		print_daily(fn(day), day)
	else:
		# Print all days
		for day in range(7):
			d = fn(day)
			print_daily(d, day)

