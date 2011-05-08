#!/usr/bin/env python
from wsgiref.util import setup_testing_defaults
from wsgiref.simple_server import make_server
import simplejson as json
import scrapers

PORT = 8000

def lunchsvall_app(environment, start_response):
	status = "200 OK"
	headers = [("Content-type", "application/json")]

	start_response(status, headers)
	daily_specials = scrapers.get_daily_specials()
	return json.dumps(daily_specials)

httpd = make_server("", PORT, lunchsvall_app)
print "Serving on port %d..." % PORT

try:
	httpd.serve_forever()
except KeyboardInterrupt:
	print "Aborting..."

