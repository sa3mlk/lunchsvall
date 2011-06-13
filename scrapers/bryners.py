#!/usr/bin/env python
# -*- encoding: utf-8 -*-

URL = "http://bryners.se"

def get_daily_specials():
	from BeautifulSoup import BeautifulSoup
	from urllib2 import urlopen
	from datetime import date
	import re

	daily_specials = {
		"name": "Bryners",
		"specials": [],
		"streetaddress": "Kyrkogatan 24, Sundsvall",
		"dataurl": URL,
		"mapurl": "http://www.hitta.se/ViewDetailsPink.aspx?Vkiid=ims%2bc70lKiXCPdGPetps6w%253d%253d"
	}

	try:
		today = date.today()
		day_index = today.weekday()
		current_day = [u"Måndag", u"Tisdag", u"Onsdag", u"Torsdag", u"Fredag"][day_index]
		current_day += " %d/%d" % (today.day, today.month)
	except IndexError:
		return daily_specials

	page = urlopen(URL)
	soup = BeautifulSoup(page)
	page.close()

	all_fonts = soup.findAll("font", {"color": "#000000"})
	index = 0
	courses = []
	for font in all_fonts:
		index += 1
		if font.text.find(current_day) == 0:
			courses = all_fonts[index:index+3]
			break

	def fix_html(s):
		# TODO: You might add more special html characters here
		chars = [("&amp;", "&"), ("&nbsp;", " ")]
		for html, char in chars:
			s = s.replace(html, char)
		return s

	daily_specials["specials"] = [fix_html(c.text) for c in courses]
	return daily_specials

def main():
	d = get_daily_specials()
	print d["name"]
	for c in d["specials"]:
		print "  ", c

if __name__ == "__main__":
	main()
