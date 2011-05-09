#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from wsgiref.simple_server import make_server
from datetime import date
import os.path
import simplejson as json
import scrapers

PORT = 8000

def lunchsvall_app(environment, start_response):
	d = date.today()
	cached_file = "cache/%d-%02d-%02d.json" % (d.year, d.month, d.day)

	ret = ""
	if os.path.isfile(cached_file):
		print "Returning cached file %s" % cached_file
		with file(cached_file) as f:
			ret = f.read()
	else:
		print "Scraping new day"
		daily_specials = scrapers.get_daily_specials()
		with file(cached_file, "w") as f:
			print "Saving cache as %s" % cached_file
			f.write(json.dumps(daily_specials))
		ret = json.dumps(daily_specials)

	status = "200 OK"
	headers = [
		("content-type", "text/plain"),
		("content-length", str(len(ret)))
	]

	start_response(status, headers)
	return [ret]

httpd = make_server("", PORT, lunchsvall_app)
print "Serving on port %d..." % PORT

try:
	httpd.serve_forever()
except KeyboardInterrupt:
	print "Aborting..."

