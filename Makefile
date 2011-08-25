help:
	@echo "Available Targets:"
	@cat Makefile | egrep '^(\w+?):' | sed 's/:\(.*\)//g' | sed 's/^/- /g'

setup:
	@pip install -r REQUIREMENTS

run:
	@PYTHONPATH=. python rockload/server.py --debug

drop:
	@rm -rf ./db_data

db:
	@mkdir -p db_data
	@mongod --dbpath ./db_data --port 12345 --rest
