#!/usr/bin/env python
# -*- encoding: utf8 -*-

from urllib2 import urlopen
import os
from datetime import date

def get_daily_specials():
	today = date.today()
	year, week = today.isocalendar()[:2]
	PDF_URL = "http://www.delinorr.se/files/Meny_Vecka_%d_%d.pdf" % (week, year)
	page = urlopen(PDF_URL)
	with file("delinorr.pdf", "wb") as f:
		f.write(page.read())

	os.system("pdf2txt.py -c utf-8 -o delinorr.txt delinorr.pdf")

	daily_specials = {
		"name": "Deli Norr",
		"specials": [],
		"streetaddress": "Nybrogatan 5, Sundsvall",
		"mapurl": "http://www.hitta.se/ViewDetailsPink.aspx?Vkiid=tURKyBsIBejyvRtSYTRetQ%253d%253d"
	}

	day_str = ""
	try:
		pdf_days = {0: "åndag", 1: "Tisdag", 2: "Onsdag", 3: "Torsdag", 4: "Fredag"}
		day_str = pdf_days[date.today().weekday()]
	except KeyError:
		return daily_specials

	collect = False
	with file("delinorr.txt") as f:
		day_len = len(day_str)
		for line in f.readlines():
			if collect:
				if len(line) > 2:
					daily_specials["specials"].append(line.strip())
					break
			if not collect and line[0:day_len] == day_str:
				collect = True

	return daily_specials

def main():
	d = get_daily_specials()
	print d["name"]
	if len(d["specials"]) == 0:
		print "No lunch today"
	else:
		for c in d["specials"]:
			print "  ", c

if __name__ == "__main__":
	main()
