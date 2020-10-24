default: install-dev

# Local pre-deploy command.
all: install-dev format-check lint typecheck unit run-debug


# Show make targets and comments.
h help:
	@egrep '(^\S)|^$$' Makefile


install-dev:
	pip install pip --upgrade
	pip install -r requirements-dev.txt --upgrade


# Run all configured tasks.
run:
	unicron/unicron.py --verbose

# Integration test.
# Run app in VERBOSE mode against the TEST VAR directory.
ig run-debug:
	cd unicron && ./test.sh


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
permission:
	chmod +x unicron/var/targets/*


# Tail the app log.
log-app:
	cd unicron/var && tail -F app.log
# Same as above but with longer history.
log-app-long:
	cd unicron/var && tail -n200 -F app.log


# Tail the task logs.
log-tasks:
	cd unicron/var && tail -F output/*.log
# Same as above but with longer history.
log-tasks-long:
	cd unicron/var && tail -n50 -F output/*.log

# Tail both the app and task logs.
log:
	cd unicron/var && tail -F output/*.log app.log
# As above, for test tasks. We make the _test_var path shown here for clarity.
log-tests:
	cd unicron && tail -n20 -F _test_var/output/*.log _test_var/app.log

format:
	black .
format-check:
	black . --diff --check

pylint:
	# Exit on error code if needed.
	pylint unicron/unicron.py || pylint-exit $$?

lint: pylint

# Apply formatting and linting fixes.
fix: format lint

typecheck:
	mypy unicron tests


# Reset tasks and logs in the test var dir.
reset:
	cd unicron && ./reset.sh

# Run unit tests.
unit: reset
	pytest


# Serve docs site.
.PHONY: docs
docs:
	docsify serve docs
