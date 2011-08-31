help:
	@echo "Available Targets:"
	@cat Makefile | egrep '^(\w+?):' | sed 's/:\(.*\)//g' | sed 's/^/- /g'

setup:
	@pip install -r REQUIREMENTS

run:
	@PYTHONPATH=. python rockload/server.py --debug

collect:
	@cd rockload && PYTHONPATH=../ aero collectstatic -o /tmp/rockload/static

drop:
	@cat ./db_data/mongod.pid | xargs kill -9
	@rm -rf ./db_data

db:
	@mkdir -p ./db_data/data
	@mongod --logpath `pwd`/db_data/mongod.log --pidfilepath `pwd`/db_data/mongod.pid --rest --port 12345 --dbpath `pwd`/db_data/data &
