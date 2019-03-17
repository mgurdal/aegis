all: test

isort:
	isort -rc


.install-deps: $(shell find requirements -type f)
	@python3 -m pip install -r requirements/dev.txt
	@touch .install-deps

.develop: .install-deps $(shell find aiohttp_auth -type f)
	@flit install --symlink
	@touch .develop

.flake: .install-deps .develop $(shell find aiohttp_auth -type f) \
                      $(shell find tests -type f)
	@flake8 .
	@touch .flake

flake: .flake

test: flake
	@pytest tests


cov: flake
	@PYTHONASYNCIODEBUG=1 pytest --cov=aiohttp_auth tests
	@pytest --cov=aiohttp_auth --cov-append --cov-report=html --cov-report=term tests
	@echo "open file://`pwd`/htmlcov/index.html"

doc:
	@make -C docs html SPHINXOPTS="-W -E"
	@echo "open file://`pwd`/docs/_build/html/index.html"
