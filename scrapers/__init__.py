import brandstation
import bryners
import delicerano
import delinorr
import gardshuset
import metropol
import invito
import lunchguiden
import max
import skonerten

def get_daily_specials():
	scrapers = [
		delicerano,
		bryners,
		delinorr,
		gardshuset,
		metropol,
		invito,
		lunchguiden,
		max,
		brandstation,
		skonerten
	]

	specials = []
	for scraper in scrapers:
		# The result can either be a list of dicts or a simple dict
		result = scraper.get_daily_specials()
		if isinstance(result, list):
			specials.extend(result)
		else:
			specials.append(result)

	# Remove all restaurants with no daily specials
	return filter(lambda x: len(x["specials"]), specials)

