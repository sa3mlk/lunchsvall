#!/usr/bin/env python
# -*- encoding: utf8 -*-

from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import date

URL = "http://www.casinocosmopol.se/sundsvall-mat-&-dryck-casinoterrassen.htm"

def get_daily_specials(day=None):
	page = urlopen(URL)
	soup = BeautifulSoup(page)
	page.close()

	daily_specials = {
		"name": "Casinoterrassen",
		"specials": [],
		"streetaddress": "Kasinoparken 1, Sundsvall",
		"dataurl": URL,
		"mapurl": "http://www.hitta.se/ViewDetailsPink.aspx?Vkiid=vQ%252frPplj%2b%252f2%2beoJQHt6vDA%253d%253d&Vkid=1690117"
	}

	if day == None:
		day = date.today().weekday()

	# No lunch on Saturday or Sunday
	if day == 5 or day == 6:
		return daily_specials

	lunch = soup.find(lambda tag: tag.name == "p" and tag.text.find("LUNCHMENY") != -1)
	menu = lunch.findNextSibling("p")

	def day_match(day):
		days = [u"M&aring;", u"Ti", u"On", u"To", u"Fr"]
		return days[day] + " | "

	s = menu.text.replace("&nbsp;", " ")
	start = s.find(day_match(day))
	if start != -1:
		if day == 4:
			# Special case for Friday since that is the last item in the content
			# of the tag we're interested in.
			daily_specials["specials"] = [s[start + len(day_match(day)):]]
		else:
			stop = s.find(day_match(day + 1))
			if stop != -1:
				daily_specials["specials"] = [s[start + len(day_match(day)):stop]]

	return daily_specials

def main():
	for day in range(5):
		d = get_daily_specials(day)
		print("%s Day %d" % (d["name"], day))
		for c in d["specials"]:
			print("  ", c)

if __name__ == "__main__":
	main()

