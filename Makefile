.PHONY: clean clean-test clean-pyc clean-build docs help
.PHONY: clean help lint test docs nixenv
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

<<<<<<< HEAD
BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	rm -rfv __pycache__/
	rm -rfv */__pycache__
	rm -rfv */**/__pycache__
	rm -rfv *.egg_info/

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

lint: ## check style with flake8
	flake8 qtc tests

test: ## run tests quickly with the default Python
	python setup.py test

test-all: ## run tests on every Python version with tox
	tox

coverage: ## check code coverage quickly with the default Python
	pytest tests
	coverage run -m pytest tests
	coverage xml -o corbertura.xml

push: coverage
	git add .
	git commit -m "auto push commit coverage"
	git push
	bash codacy.sh report -r corbertura.xml

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/qtc.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ qtc
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

servedocs: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

release: dist ## package and upload a release
	twine upload dist/*

dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean ## install the package to the active Python's site-packages
	python setup.py install
=======
define FIX_BIN_VERSION_FILES
import os, shutil
from pathlib import Path
from torrentfile.version import __version__ as version
for item in Path("./dist").iterdir():
	if item.is_dir() and item.name == "torrentfile_linux":
		name = name = f"TorrentFile-{version}-portable_linux"
		path = item.parent / name
		shutil.move(item, path)
		shutil.make_archive(path, 'zip', path)
	if item.is_dir() and item.name == 'torrentfile':
		name = f"TorrentFile-{version}-portable_win"
		path = item.parent / name
		shutil.move(item, path)
		shutil.make_archive(path, 'zip', path)
	elif item.name == "torrentfile" and item.is_file():
		name = f"torrentfile-{version}-linux_exec"
		path = item.parent / name
		os.rename(item, path)
	elif item.suffix == ".exe":
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
	rm -f coverage.xml
	rm -fr htmlcov/
	rm -rf *.egg-info
	rm -f corbertura.xml
	rm -fr .pytest_cache
	rm -f *.spec

test: ## Get coverage report
	pytest --cov=torrentfile --cov=tests

lint:
	black torrentfile tests
	isort torrentfile tests
	prospector torrentfile
	prospector tests

docs: ## Regenerate docs from changes
	rm -rf docs/*
	mkdocs -q build
	touch docs/.nojekyll

coverage: test ## Get coverage report
	coverage html
	coverage xml

push: clean lint docs test ## Push to github
	git add .
	git commit -m "$m"
	git push

setup: clean docs ## setup and build repo
	pip install --pre --upgrade --force-reinstall --no-cache -rrequirements.txt
	python setup.py sdist bdist_wheel bdist_egg
	pip install -e .
	twine upload --verbose dist/*

build: clean
	pip install --pre --upgrade --force-reinstall --no-cache -rrequirements.txt
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

nixenv: ## activate unix python vurtual environment
	source nixenv/bin/activate

nixbuild:
	pip install pyinstaller
	python3 setup.py sdist bdist_wheel bdist_egg
	pip install -e .
	rm -rfv ../runner
	mkdir ../runner
	touch ../runner/exec
	cp ./assets/favicon.png ../runner/favicon.png
	@echo "import torrentfile" >> ../runner/exec
	@echo "torrentfile.main()" >> ../runner/exec
	pyinstaller --distpath ../runner/dist --workpath ../runner/build \
		-F -n torrentfile -c -i ../runner/favicon.png \
		--specpath ../runner/ ../runner/exec
	pyinstaller --distpath ../runner/dist --workpath ../runner/build \
		-D -n torrentfile_linux -c -i ../runner/favicon.png \
		--specpath ../runner/ ../runner/exec
	cp -rfv ../runner/dist/* ./dist/
	python3 -c "$$FIX_BIN_VERSION_FILES"
>>>>>>> a987bef42cd0e88ec6a5fdcb5327e72946e49de2
