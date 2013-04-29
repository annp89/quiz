MANAGE=python manage.py

test=

run:
	$(MANAGE) runserver

syncdb:
	$(MANAGE) syncdb

initmigration:
	$(MANAGE) schemamigration --init $(app)

schemamigration:
	$(MANAGE) schemamigration --auto $(app)

migrate:
	$(MANAGE) migrate $(APP)

manage:
	$(MANAGE) $(ARGS)

shell:
	$(MANAGE) shell

clean:
	find . -name "*.pyc" -exec rm -rf {} \;