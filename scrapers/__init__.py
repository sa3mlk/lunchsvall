import brandstation
import bryners
import delicerano
import delinorr
import gardshuset
import invito
import lunchguiden
import max
import skonerten

def get_daily_specials():
	scrapers = [
		delicerano,
		brandstation,
		bryners,
		delinorr,
		gardshuset,
		invito,
		lunchguiden,
		max,
		skonerten
	]

	specials = []
	for scraper in scrapers:
		result = scraper.get_daily_specials()
		if isinstance(result, list):
			specials.extend(result)
		else:
			specials.append(result)

	return specials

