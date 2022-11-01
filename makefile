CURLFLAGS = -X POST -s --data-urlencode 'input@website/functions.js'
PYSRC = cache.py lunch.py refresh.py
JSMIN = website/functions.min.js

all: validate $(JSMIN)

$(JSMIN): website/functions.js
	@echo Minifying $@
	@curl $(CURLFLAGS) http://javascript-minifier.com/raw > $@

validate: $(PYSRC)
	@pipenv run python3 -m py_compile $(PYSRC)

clean:
	@rm $(JSMIN)

