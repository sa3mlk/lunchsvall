#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from datetime import date
import os

def format_cache_file():
	d = date.today()
	cached_file = "cache/{y}/{m:02}/{d}.json".format(y=d.year, m=d.month, d=d)
	cache_dir = os.path.dirname(cached_file)
	base_path = os.path.dirname(os.path.realpath(__file__))
	return [base_path + "/" + p for p in (cached_file, cache_dir)]

if __name__ == "__main__":
	f, d = format_cache_file()
	print("cache_file: {f}\ncache dir: {d}".format(f=f, d=d))
	exit(0)

