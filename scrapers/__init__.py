import scrapers.augustas
import scrapers.biteline
import scrapers.bilbiten
import scrapers.bryners
import scrapers.delinorr
import scrapers.estreet
import scrapers.traktoren
import scrapers.gardshuset
import scrapers.himlabadet
import scrapers.fernaeus
import scrapers.nojet
import scrapers.oasen
import scrapers.opus
import scrapers.invito
import scrapers.kalabra
import scrapers.knaust
import scrapers.lacodicomo
import scrapers.lunchguide
import scrapers.mittgastronomi
import scrapers.mokajen
import scrapers.norrlandskallaren
import scrapers.svartviksherrgard
import scrapers.skonsmon
import scrapers.tantanci
import scrapers.dolcetto
import scrapers.max
import scrapers.wretmans
import scrapers.brandstation

import sys, traceback
import simplejson as json

def get_scrapers():
	return [
		scrapers.biteline,
		scrapers.oasen,
		scrapers.opus,
		scrapers.invito,
		scrapers.augustas,
		scrapers.nojet,
		scrapers.bryners,
		scrapers.mokajen,
		scrapers.tantanci,
		scrapers.estreet,
		scrapers.traktoren,
		scrapers.delinorr,
		scrapers.gardshuset,
		scrapers.himlabadet,
		scrapers.fernaeus,
		scrapers.kalabra,
		scrapers.knaust,
		scrapers.lacodicomo,
		scrapers.lunchguide,
		scrapers.mittgastronomi,
		scrapers.norrlandskallaren,
		scrapers.svartviksherrgard,
		scrapers.skonsmon,
		scrapers.dolcetto,
		scrapers.max,
		scrapers.wretmans,
		scrapers.bilbiten,
		scrapers.brandstation,
	]

def get_daily_specials():
	specials = []
	for scraper in get_scrapers():
		# The result can either be a list of dicts or a simple dict
		try:
			result = scraper.get_daily_specials()
			# Try to convert so json for sanity reasons, if it fails then skip
			# that scraper result.
			json.dumps(result)
		except Exception as e:
			traceback.print_exc(file=sys.stderr)
			print("*"*80, file=sys.stderr)
		else:
			if isinstance(result, list):
				specials.extend(result)
			else:
				specials.append(result)

	# Remove all restaurants with no daily specials
	return list(filter(lambda x: len(x["specials"]), specials))

