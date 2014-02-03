#!/usr/bin/env python
# -*- encoding: utf8 -*-

# This motherfucker requires PDFMiner installed
# http://www.unixuser.org/~euske/python/pdfminer/index.html

from urllib2 import urlopen
import sys
import os
import os.path
from subprocess import Popen
from datetime import date
import re

def get_daily_specials(day=None):
	PDF_URL = "http://brandstation.grankotten.com/lunch_brandstation.pdf"
	page = urlopen(PDF_URL)
	with file("brandstation.pdf", "wb") as f:
		f.write(page.read())

	daily_specials = {
		"name": "Brandstation",
		"specials": [],
		"streetaddress": "Köpmangatan 29, Sundsvall",
		"dataurl": PDF_URL,
		"mapurl": "http://www.hitta.se/ViewDetailsPink.aspx?Vkiid=3LhMg0f89wskR4cV3PAzfA%253d%253d&Vkid=1622144"
	}

	if day == None:
		day = date.today().weekday()

	try:
		p = Popen("pdf2txt.py -c utf-8 -o brandstation.txt brandstation.pdf", shell=True)
		os.waitpid(p.pid, 0)[1]
	except OSError:
		print >> sys.stderr, "Seems like you don't have PDFMiner installed."
		raise

	if not os.path.isfile("brandstation.txt"):
		return daily_specials

	try:
		day = ["Måndag", "Tisdag", "Onsdag", "Torsdag", "Fredag"][day]
	except KeyError:
		return daily_specials

	def fix_whitespace(line):
		line = line.replace("\t", "").replace("\r", "")
		line = line.replace("\xc2", "").replace("\xa0", "")
		return line

	lines = map(lambda x: x.strip(), open("brandstation.txt").readlines())
	for i, l in enumerate(lines):
		if l == day:
			daily_specials["specials"] = lines[i+1:i+4]
			break;

	return daily_specials

def main():
	for day in range(5):
		d = get_daily_specials(day)
		print "%s day %d" % (d["name"], day)
		if len(d["specials"]) == 0:
			print "No lunch today"
		else:
			for c in d["specials"]:
				print "  ", c

if __name__ == "__main__":
	main()

