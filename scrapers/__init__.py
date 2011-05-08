import brandstation
import bryners
import delicerano
import delinorr
import invito
import lunchguiden
import max
import skonerten

def get_daily_specials():
	scrapers = [
		brandstation,
		bryners,
		delicerano,
		delinorr,
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

