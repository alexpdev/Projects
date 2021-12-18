.PHONY: clean help full lint build environment test docs push
.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

define FIX_BIN_VERSION_FILES
import os
import shutil
from pathlib import Path
from torrentfile.version import __version__ as version

for item in Path("./dist").iterdir():
	if item.is_dir() and item.name == 'torrentfile':
		name = f"TorrentFile-{version}-portable_win"
		path = item.parent / name
		shutil.move(item, path)
		shutil.make_archive(path, 'zip', path)

	if item.suffix == ".exe":
		newname = f"{item.stem}-{version}-portable.exe"
		full = item.parent / newname
		os.rename(item, full)
endef
export FIX_BIN_VERSION_FILES

BROWSER := python -c "$$BROWSER_PYSCRIPT"


help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	@echo Cleaning
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	rm -fr .tox/
	rm -f .coverage
	rm -rf */__pycache__
	rm -fr htmlcov/
	rm -rf *.egg-info
	rm -f corbertura.xml
	rm -fr .pytest_cache
	rm -f *.spec

lint:
	pip install pyroma bandit black isort prospector
	black torrentfile tests
	isort torrentfile tests
	prospector torrentfile
	prospector tests

docs: ## Regenerate docs from changes
	pip install mkdocs mkdocs-material mkdocstrings
	rm -rf docs/*
	mkdocs -q build
	touch docs/.nojekyll

push: clean lint docs ## Push to github
	pytest
	git add .
	git commit -m "$m"
	git push

setup: clean ## setup and build repo
	pip install --pre --upgrade --force-reinstall --no-cache -rrequirements.txt
	python setup.py sdist bdist_wheel bdist_egg
	pip install -e .
	twine upload dist/*

winbuild: clean
	pip install pyinstaller
	python setup.py sdist bdist_wheel bdist_egg
	rm -rfv ../runner
	mkdir ../runner
	touch ../runner/exe
	cp ./assets/favicon.ico ../runner/favicon.ico
	@echo "import torrentfile" >> ../runner/exe
	@echo "torrentfile.main()" >> ../runner/exe
	pyinstaller --distpath ../runner/dist --workpath ../runner/build \
		-F -n torrentfile -c -i ../runner/favicon.ico \
		--specpath ../runner/ ../runner/exe
	pyinstaller --distpath ../runner/dist --workpath ../runner/build \
		-D -n torrentfile -c -i ../runner/favicon.ico \
		--specpath ../runner/ ../runner/exe
	cp -rfv ../runner/dist/* ./dist/
	python -c "$$FIX_BIN_VERSION_FILES"


nixbuild: clean install
	pip install pyinstaller
	python3 setup.py sdist bdist_wheel bdist_egg
	rm -rfv ../runner
	mkdir ../runner
	touch ../runner/exec
	cp ./assets/favicon.png ../runner/favicon.png
	@echo "import torrentfile" >> ../runner/exec
	@echo "torrentfile.main()" >> ../runner/exec
	pyinstaller --distpath ../runner/dist --workpath ../runner/build \
		-F -n torrentfile -c -i ../runner/favicon.png \
		--specpath ../runner/ ../runner/exec
	cp -rfv ../runner/dist/* ./dist/
