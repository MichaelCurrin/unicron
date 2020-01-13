# Show commands and exit.
help:
	@egrep '(^\S)|^$$' Makefile


# Install dev dependencies.
dev-install:
	pip install pip --upgrade
	pip install -r requirements-dev.txt


# Run make application in verbose mode.
run:
	cd unicron && ./unicron.py -v


# Run app in verbose mode against test var directory.
test-output:
	cd unicron && ./test.sh


# Tail the log files.
log:
	cd unicron/var && tail -F output/*.log app.log

# Tail the test logs.
log-test:
	cd unicron/_test_var && tail -F output/*.log app.log


# Apply Black formatting to Python files.
format:
	black . -l 79

# Lint with Pylint.
lint:
	pylint unicron/unicron.py

check: format lint


# Make all tasks executable.
p permission:
	chmod +x unicron/var/targets/*
