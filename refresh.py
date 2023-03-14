# -*- encoding: utf-8 -*-

import os
from cache import format_cache_file

def main():
	cache_file = format_cache_file()[0]
	os.remove(cache_file)
	return 0

if __name__ == "__main__":
	exit(main())

