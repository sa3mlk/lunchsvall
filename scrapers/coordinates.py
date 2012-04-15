#!/usr/bin/env python
# -*- encoding: utf-8 -*-

coordinates = {
	# Restaurant: (latitude, longitude)
	"Bryners": (62.3908, 17.3042),
	"Delicerano": (62.3912, 17.3124),
	"Deli Norr": (0, 0),
	"Opus Restaurang & Pianobar": (0, 0),
	"Fernaeus Gastronomiska": (0, 0),
	"Metropol Restaurang & Café": (0, 0),
	"Invito": (0, 0),
	"Laco di Como": (0, 0),
	"Aveny": (0, 0),
	"Birstabaren": (0, 0),
	"Bite Line Centralstationen": (0, 0),
	"Bite Line City": (0, 0),
	"Bite Line West": (0, 0),
	"Café Basilica": (0, 0),
	"Elite Hotel Knaust": (0, 0),
	"Innergården": (0, 0),
	"Kitchen Theatre": (0, 0),
	"Lasses Matstuga": (0, 0),
	"Restaurang Arena": (0, 0),
	"Restaurang Cupolen": (0, 0),
	"Restaurang E.ON Arena": (0, 0),
	"Restaurang Etage": (0, 0),
	"Restaurang Hornet": (0, 0),
	"Restaurang Parkcafé": (0, 0),
	"Restaurang Skönsberg Folkets Hus": (0, 0),
	"Restaurang Vinkeln": (0, 0),
	"Saffrans Bodega": (0, 0),
	"Scandic Nord": (0, 0),
	"Spisa hos Liza": (0, 0),
	"Stadshuset": (0, 0),
	"Tant Anci & Fröken Sara": (0, 0),
	"Villa Marieberg": (0, 0),
	"Vin & Matfabriken": (0, 0),
	"Ågläntan": (0, 0),
	"Mitt Gastronomi": (0, 0),
	"Svartviks Herrgård": (0, 0),
	"Dolcetto": (0, 0),
	"mAx": (0, 0),
	"Wretmans": (0, 0),
	"Wretmans City": (0, 0),
	"Bite Line": (0, 0),
	"Restaurang Bilbiten": (0, 0),
	"Skonerten": (0, 0)
}

def get_coordinate(restaurant):
	try:
		return coordinates[restaurant]	
	except KeyError:
		return (None, None)

if __name__ == "__main__":
	from sys import argv
	print get_coordinate(argv[1])

