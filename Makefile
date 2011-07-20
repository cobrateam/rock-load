run:
	@env PYTHONPATH=. python rockload/server.py

syncdb:
	@mysql -u root < ./db/createdb.sql
	@mysql -u root rockload < ./db/initial.sql
