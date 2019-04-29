all: test

isort:
	isort -rc


.install-deps: $(shell find requirements -type f)
	@python3 -m pip install -r requirements/dev.txt
	@touch .install-deps

.develop: .install-deps $(shell find aegis -type f)
	@flit install --symlink
	@touch .develop

.flake: .install-deps .develop $(shell find aegis -type f) \
                      $(shell find tests -type f)
	@flake8 .
	@touch .flake

flake: .flake

test: flake
	@pytest tests

cov: flake
	@PYTHONASYNCIODEBUG=1 pytest --cov=aegis tests
	@pytest --cov=aegis --cov-append --cov-report=html --cov-report=term tests
	@echo "open file://`pwd`/htmlcov/index.html"
