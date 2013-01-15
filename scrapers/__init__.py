import bilbiten
import bryners
import curryhouse
import delinorr
import delicerano
import casinoterrassen
import opus
import fernaeus
import metropol
import invito
import jops
import lacodicomo
import lunchguiden
import mittgastronomi
import norrlandskallaren
import svartviksherrgard
import dolcetto
import max
import wretmans
import brandstation
import skonerten

import sys, traceback
import simplejson as json

def get_daily_specials():
	scrapers = [
		curryhouse,
		bryners,
		delinorr,
		delicerano,
		casinoterrassen,
		opus,
		fernaeus,
		metropol,
		invito,
		jops,
		lacodicomo,
		lunchguiden,
		mittgastronomi,
		norrlandskallaren,
		svartviksherrgard,
		dolcetto,
		max,
		wretmans,
		bilbiten,
		brandstation,
		skonerten
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

