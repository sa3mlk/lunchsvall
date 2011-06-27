import bryners
import delicerano
import delinorr
import gardshuset
import metropol
import invito
import jops
import lunchguiden
import mittgastronomi
import svartviksherrgard
import dolcetto
import max
import brandstation
import skonerten

import sys, traceback

def get_daily_specials():
	scrapers = [
		delicerano,
		bryners,
		delinorr,
		gardshuset,
		metropol,
		invito,
		jops,
		lunchguiden,
		mittgastronomi,
		svartviksherrgard,
		dolcetto,
		max,
		brandstation,
		skonerten
	]

	specials = []
	for scraper in scrapers:
		# The result can either be a list of dicts or a simple dict
		try:
			result = scraper.get_daily_specials()
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

