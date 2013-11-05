import bilbiten
import bryners
import delicerano
import delinorr
import gardshuset
import opus
import fernaeus
import metropol
import invito
import jops
import lunchguiden
import mittgastronomi
import norrlandskallaren
import svartviksherrgard
import skonsmon
import dolcetto
import max
import wretmans
import brandstation

import sys, traceback
import simplejson as json

def get_daily_specials():
	scrapers = [
		bryners,
		delicerano,
		delinorr,
		opus,
		gardshuset,
		fernaeus,
		metropol,
		invito,
		jops,
		lunchguiden,
		mittgastronomi,
		norrlandskallaren,
		svartviksherrgard,
		skonsmon,
		dolcetto,
		max,
		wretmans,
		bilbiten,
		brandstation,
	]

	specials = []
	for scraper in scrapers:
		# The result can either be a list of dicts or a simple dict
		try:
			result = scraper.get_daily_specials()
			# Try to convert so json for sanity reasons, if it fails then skip
			# that scraper result.
			json.dumps(result)
		except Exception, e:
			traceback.print_exc(file=sys.stderr)
			print >> sys.stderr, "*"*80
		else:
			if isinstance(result, list):
				specials.extend(result)
			else:
				specials.append(result)

	# Remove all restaurants with no daily specials
	return filter(lambda x: len(x["specials"]), specials)

