#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from urllib2 import urlopen, URLError
from sys import argv
import simplejson as json

SERVER = "http://127.0.0.1:8000"

def main():
	try:
		page = urlopen(SERVER)
		data = json.load(page)
		page.close()
	except URLError as e:
		print e
		exit(1)

	for i in data:
		if not i["specials"]:
			continue

		def print_specials():
			print i["name"]
			for j in i["specials"]:
				print "  ", j

		if len(argv) == 2 and (argv[1].lower() in i["name"].lower()):
			print_specials()
		elif len(argv) == 1:
			print_specials()
		else:
			pass

if __name__ == "__main__":
	main()
