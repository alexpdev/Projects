.PHONY: clean, tests
.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys
for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print(f"{target}-20s {help}")
endef
export PRINT_HELP_PYSCRIPT

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build ## remove all build, test, coverage and artifacts

clean-build:
	@echo Cleaning
	rm -rf *.torrent

test: clean ## Test torrentfilejs command line;
	@echo Test1
	node index.js --private --source source1 --t url1 url2 --metaversion 1 -p dir

test2: clean ## Test torrenfilejs cli 2
	@echo Test2
	node index.js --piecelength 18 --comment "some comment" -p dir \
	--metaversion 2 --announce url2 url3 url5 --out dir2.torrent

tests: test test2 ## Testing both tests
