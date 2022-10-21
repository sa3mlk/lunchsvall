#!/usr/bin/python3
# -*- encoding: utf-8 -*-

import os
import simplejson as json
import scrapers
from datetime import date
from cache import format_cache_file
from bottle import route, run, response, request

PORT = 40000

@route('/')
def index():
	cached_file, cache_dir = format_cache_file()

	if not os.path.exists(cache_dir):
		os.makedirs(cache_dir)

	ret = ""
	if os.path.isfile(cached_file):
		with open(cached_file) as f:
			ret = f.read()
	else:
		print("Scraping new day")
		daily_specials = scrapers.get_daily_specials()
		with open(cached_file, "w") as f:
			print("Saving cache as %s" % cached_file)
			f.write(json.dumps(daily_specials))
		ret = json.dumps(daily_specials)

	content_type = 'application/json'
	if request.query.callback:
		ret = "{cb}({json});".format(cb=request.query.callback, json=ret)
		content_type = 'application/javascript'

	print(request.environ.get('REMOTE_ADDR'))

	response.set_header('Access-Control-Allow-Origin', '*')
	response.set_header('Access-Control-Allow-Headers', 'x-requested-with')
	response.content_type = content_type + '; charset=UTF8'
	return ret

run(server='cheroot', host='0.0.0.0', port=PORT)
