# Show commands and exit.
help:
	@egrep '(^\S)|^$$' Makefile


# Install dev dependencies.
dev-install:
	pip install pip --upgrade
	pip install -r requirements-dev.txt


# Run make application.
run:
	cd unicron && ./unicron.py


# Run app against test directory.
test-output:
	cd unicron && ./test.sh


# Tail the log files.
log:
	cd unicron/var && tail -f output/*.log app.log

# Tail the test logs.
log-test:
	cd unicron/_test_var && tail -f output/*.log app.log


# Apply Black formatting to Python files.
fmt:
	black . -l 79
