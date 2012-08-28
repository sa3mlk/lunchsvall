#!/usr/bin/env python
# -*- encoding: utf-8 -*-

coordinates = {
	# Restaurant: (latitude, longitude in WGS 84 decimal format)
	"Aveny": (62.38633, 17.30678),
	"Birstabaren": (62.44521, 17.32036),
	"Bite Line Centralstationen": (62.38692, 17.31550),
	"Bite Line City": (62.38875, 17.30879),
	"Bite Line West": (62.39311, 17.26825),
	"Bryners": (62.3908, 17.3042),
	"Café Basilica": (0, 0),
	"Deli Norr": (62.39098, 17.31181),
	"Delicerano": (62.3912, 17.3124),
	"Dolcetto": (62.38984, 17.31263),
	"Elite Hotel Knaust": (62.39055, 17.31129),
	"Fernaeus Gastronomiska": (62.37660, 17.34571),
	"Innergården": (62.39141, 17.30774),
	"Invito": (62.39056, 17.31306),
	"Kitchen Theatre": (62.39182, 17.30587),
	"Laco di Como": (62.44869, 17.33029),
	"Lasses Matstuga": (62.39587, 17.33584),
	"Metropol Restaurang & Café": (62.39703, 17.28086),
	"Mitt Gastronomi": (62.42071, 17.21555),
	"Opus Restaurang & Pianobar": (62.39070, 17.31188),
	"Restaurang Arena": (62.39373, 17.30033),
	"Restaurang Bilbiten": (62.38985, 17.27697),
	"Restaurang Cupolen": (62.44675, 17.33145),
	"Restaurang E.ON Arena": (62.50609, 17.34980),
	"Restaurang Etage": (0, 0),
	"Restaurang Hornet": (0, 0),
	"Restaurang Parkcafé": (0, 0),
	"Restaurang Skönsberg Folkets Hus": (0, 0),
	"Restaurang Vinkeln": (0, 0),
	"Saffrans Bodega": (0, 0),
	"Scandic Nord": (0, 0),
	"Skonerten": (0, 0),
	"Spisa hos Liza": (0, 0),
	"Stadshuset": (0, 0),
	"Svartviks Herrgård": (0, 0),
	"Tant Anci & Fröken Sara": (0, 0),
	"Villa Marieberg": (0, 0),
	"Vin & Matfabriken": (0, 0),
	"Wretmans City": (0, 0),
	"Wretmans": (0, 0),
	"mAx": (0, 0),
	"Ågläntan": (0, 0)
}

def get_coordinate(restaurant):
	try:
		return coordinates[restaurant]	
	except KeyError:
		return (None, None)

if __name__ == "__main__":
	from sys import argv
	print get_coordinate(argv[1])

