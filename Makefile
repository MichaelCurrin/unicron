# Show make targets and comments then exit.
help:
	@egrep '(^\S)|^$$' Makefile


# Install dev dependencies.
dev-install:
	pip install pip --upgrade
	pip install -r requirements-dev.txt


# Use Unicron to run all configured tasks.
run:
	unicron/unicron.py --verbose

# Run app in VERBOSE mode against the TEST VAR directory.
run-test:
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


# Make all tasks executable.
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


# Apply Black formatting to Python files.
format:
	black .

# Lint with Pylint.
lint:
	pylint unicron/unicron.py

# Apply formatting and lint.
c check: format lint


# Reset tasks and logs in the test var dir.
reset:
	cd unicron && ./reset.sh

# Run unit tests.
unit: reset
	pytest

.PHONY: docs
# Serve docs site.
docs:
	docsify serve docs
