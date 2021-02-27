default: install-dev

# Local pre-release step.
all: install-dev fmt-check lint typecheck unit


# Show make targets and comments.
h help:
	@egrep '(^\S)|^$$' Makefile


install-dev:
	pip install pip --upgrade
	pip install -r requirements-dev.txt

upgrade:
	pip install pip --upgrade
	pip install -r requirements-dev.txt --upgrade


# Run all configured tasks in main VAR targets dir.
run:
	python3 -m unicron.unicron --verbose

run-quiet:
	python3 -m unicron.unicron


# View configured tasks.
ls-tasks:
	ls -l unicron/var/targets/
ls-test-tasks:
	ls -l unicron/_test_var/targets/

# View last run dates for configured tasks.
ls-runs:
	cd unicron/var/last_run/ && tail *
ls-test-runs:
	cd unicron/_test_var/last_run/ && tail *


# Make all task scripts executable.
perms:
	chmod +x unicron/var/targets/*


# Tail the app logs.
log-app:
	cd unicron/var && tail -F app.log
# Same as above but with longer history.
log-app-long:
	cd unicron/var && tail -n200 -F app.log


# Tail the task logs.
log-tasks:
	cd unicron/var && tail -F output/*.log
log-tasks-long:
	cd unicron/var && tail -n50 -F output/*.log

# Tail both the app and task logs.
log:
	cd unicron/var && tail -F output/*.log app.log
# Tail logs created by `debug` target.
log-tests:
	cd unicron/_test_var && tail -n20 -F output/*.log app.log


fmt:
	black .
	isort .
fmt-check:
	black . --diff --check
	isort . --check-only

pylint:
	# Exit on error code on a fail. Expand failure to all non-fatal messages too.
	pylint unicron tests || pylint-exit -efail -wfail -rfail -cfail $$?

lint: pylint

fix: fmt lint

t typecheck:
	mypy unicron tests


# Reset tasks and logs in the TEST VAR dir.
reset:
	bin/reset.sh

# Run unit tests.
unit: reset
	TEST=true pytest
test-coverage: reset
	TEST=true coverage run --source=unicron -m pytest

test-report:
	coverage report -m

test: test-coverage test-report

# Run tests and serve coverage output explorer.
test-html: test-coverage
	coverage html
	npx docsify serve htmlcov


# Integration tests. Requires manual inspection.
debug: reset
	bin/test.sh


clean:
	find . -name '*.pyc' -delete


# Serve docs site.
.PHONY: docs
docs:
	npx docsify serve docs
