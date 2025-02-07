.PHONY: install virtenv ipython test testci watch flake8 clean


install: virtenv
	@echo "Installing for dev and test environments - Development Mode (a.k.a. “Editable Installs”)"
	@.venv/bin/python -m pip install -e '.[test,dev]'


virtenv:
	@python3 -m venv .venv
	@.venv/bin/python -m pip install --upgrade pip


ipython:
	@.venv/bin/ipython


test:
	@.venv/bin/pytest -s


watch:
	# @.venv/bin/ptw -- -vv -s
	@ls **/*.py | entr pytest


lint:
	@.venv/bin/pflake8


fmt:
	@.venv/bin/isort --profile black .
	@.venv/bin/black .


# Clean unused files.
clean:
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name '__pycache__' -exec rm -rf {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
	@rm -rf .cache
	@rm -rf .pytest_cache
	@rm -rf .mypy_cache
	@rm -rf build
	@rm -rf dist
	@rm -rf *.egg-info
	@rm -rf htmlcov
	@rm -rf .tox/
	@rm -rf docs/_build
