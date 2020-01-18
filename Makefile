# Show commands and exit.
help:
	@egrep '(^\S)|^$$' Makefile


# Install dev dependencies.
dev-install:
	pip install pip --upgrade
	pip install -r requirements-dev.txt


# Run main application.
run:
	unicron/unicron.py --verbose


# Run app in verbose mode against test var directory.
o test-output:
	cd unicron && ./test.sh


# Tail the log files.
log:
	cd unicron/var && tail -F output/*.log app.log

# Tail the test logs.
log-test:
	cd unicron/_test_var && tail -F output/*.log app.log


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

# Make all tasks executable.
permission:
	chmod +x unicron/var/targets/*
