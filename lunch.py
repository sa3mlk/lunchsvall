#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from wsgiref.simple_server import make_server
from datetime import date
import os
import simplejson as json
import scrapers
from cache import format_cache_file

PORT = 40000

def lunchsvall_app(environment, start_response):
	if environment["PATH_INFO"] != "/":
		print "Ignoring:", environment["PATH_INFO"]
		start_response("404 NOT FOUND", [("content-type", "text/plain")])
		return [":-("]

	cached_file, cache_dir = format_cache_file()

	if not os.path.exists(cache_dir):
		os.makedirs(cache_dir)

	ret = ""
	if os.path.isfile(cached_file):
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
		("Content-Type", "application/json"),
		("Content-Length", str(len(ret))),
		("Access-Control-Allow-Origin", "*")
	]

	start_response(status, headers)
	return [ret]

httpd = make_server("", PORT, lunchsvall_app)
print "Serving on port %d..." % PORT

try:
	httpd.serve_forever()
except KeyboardInterrupt:
	print "Aborting..."


