help:
	@egrep '(^\S)|^$$' Makefile

run:
	cd unicron && ./unicron.sh

test:
	cd unicron && ./test.sh

log:
	cd unicron/var && tail -f output/*.log app.log
log-test:
	cd unicron/_test_var && tail -f output/*.log app.log
