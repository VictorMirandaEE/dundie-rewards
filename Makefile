.PHONY: install venv ipython test watch lint format clean docs docs-serve build publish-test publish


# Install for dev and test environments - Development Mode (a.k.a. “Editable Installs”).
install: venv
	@echo "Installing for dev and test environments - Development Mode (a.k.a. “Editable Installs”)"
	@.venv/bin/python -m pip install -e '.[test,dev]'


# Create a Python virtual environment and upgrade pip.
venv:
	@python3 -m venv .venv
	@.venv/bin/python -m pip install --upgrade pip


# Run ipython.
ipython:
	@.venv/bin/ipython


# Run tests using pytest.
test:
	@.venv/bin/pytest -s --forked


# Watch for changes and run tests.
watch:
	# @.venv/bin/ptw -- -vv -s
	@ls **/*.py | entr pytest -s --forked


# Lint code using flake8.
lint:
	@.venv/bin/mypy --ignore-missing-imports --show-error-codes dundie
	@.venv/bin/pflake8


# Format code using isort and black.
format:
	@.venv/bin/isort --profile black .
	@.venv/bin/black .


# Clean unused files.
clean:
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -depth -name '__pycache__' -exec rm -rf {} \;
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


# Build documentation using mkdocs.
docs:
	@@.venv/bin/mkdocs build --clean


# Publish documentation using mkdocs in a local server.
docs-serve:
	@@.venv/bin/mkdocs serve


# Build and generate distribution files in .egg and .whl formats.
build:
	@.venv/bin/python -m build --sdist --wheel


# Publish module package to test pypi.
publish-test:
	@twine upload --repository testpypi dist/* --verbose


# Publish module package to pypi.
publish:
	@twine upload dist/* --verbose
